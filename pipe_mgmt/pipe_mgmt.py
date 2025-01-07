class PipeMgmt:
    """
    Class for managing pipelines and their relationships.

    Provides methods for creating, searching and analyzing pipelines.

    The term "pipeline tree" refers a list of dictionaries object, where each
    dictionary represents a pipeline with its attributes and children. Note
    that the pipeline children has the same structure as a pipeline tree (i.e.,
    `list[dict]`).
    """

    pipe_key_types = {
        "name": str,
        "shortname": None | str,
        "description": None | str,
        "creation_date": None | str,
        "path": str,
        "parent": None | str,
        "children": None | list,
    }

    def __init__(self, pipe_tree=None):
        self.pipe_template = dict.fromkeys(self.pipe_key_types.keys())
        self.pipe_tree = pipe_tree
        if pipe_tree is not None:
            is_valid = all(self.validate_pipe(pipe) for pipe in pipe_tree)
            if not is_valid:
                raise ValueError("Invalid pipeline tree structure")

    def _filter_pipetree(self, pipe_tree: list[dict], attrib="name"):
        """
        Filter pipeline tree based on an attribute key.

        The dictionary representing a pipeline with children has the following
        structure: `{kwargs, children: list}`. The output of this function will
        return `[[val_parent, [[val_child1, [[val_grandchild1, ...]], ...]]]]`.
        """
        out_lst = []
        for pipe in pipe_tree:
            filtered_pipe = [pipe[attrib]]
            if pipe.get("children"):
                filtered_pipe.append(self._filter_pipetree(pipe["children"], attrib))
            out_lst.append(filtered_pipe)
        return out_lst

    def _flatten_filtered_pipetree(self, nested_list: list[list]):
        """Flatten a nested list produced by `_filter_pipetree`."""
        paths = []
        for node in nested_list:
            if len(node) == 1:  # Check if it's a terminal node
                paths.append(node)
            else:  # Non-terminal nodes have format `[val, [[val, ...]]]`
                for member in self._flatten_filtered_pipetree(node[1]):
                    paths.append([node[0]] + member)
        return paths

    def list_paths(self, pipe_tree, attrib="name"):
        """List all pipeline paths."""
        filtered_tree = self._filter_pipetree(pipe_tree, attrib)
        return self._flatten_filtered_pipetree(filtered_tree)

    def validate_pipe(self, pipe: dict) -> bool:
        """
        Validate pipeline structure and types.

        - TODO: Use `TypedDict` for type checking.
        """
        for key, expected_type in self.pipe_key_types.items():
            if key not in pipe:
                print("Key missing:", key)
                return False
            if not isinstance(pipe[key], expected_type):
                print("Key type mismatch:", key)
                return False
            if pipe["children"] is not None:
                for child in pipe["children"]:
                    if not self.validate_pipe(child):
                        return False
        return True

    def create_pipe(self, name: str, **kwargs) -> dict:
        """Create a pipeline."""
        pipe = self.pipe_template.copy()
        pipe.update(name=name, **kwargs)
        return pipe

    def get_terminal_pipes(self, pipe_tree: list[dict]) -> list[dict]:
        """Get terminal pipelines from a pipeline tree."""
        terminals = []
        for pipe in pipe_tree:
            if pipe.get("children"):
                terminals.extend(self.get_terminal_pipes(pipe["children"]))
            else:
                terminals.append(pipe)
        return terminals

    def search_pipe(self, pipe_tree: list[dict], conditions: dict) -> list[dict]:
        """Search for a pipe that matches conditions."""
        matches = []
        for pipe in pipe_tree:
            if all(pipe.get(key, None) == value for key, value in conditions.items()):
                matches.append(pipe)
            else:
                if pipe.get("children"):
                    matches.extend(self.search_pipe(pipe["children"], conditions))
        return matches

    def get_descendants(self, pipe: dict) -> list:
        """List the descendant names of a pipe recursively."""
        descendants = [pipe["name"]]
        if children := pipe.get("children"):
            for child in children:
                descendants.extend(self.get_descendants(child))
        return descendants
