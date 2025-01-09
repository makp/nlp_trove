import uuid

import yaml


class Pipe:
    """
    Class for managing individual pipelines.

    Individual pipelines are represented as dictionaries.
    """

    pipe_key_types = {
        "id": str,
        "name": str,
        "shortname": None | str,
        "description": None | str,
        "creation_date": None | str,
        "path": str,
        "parent": None | str,
        "children": None | list,
    }

    def __init__(self):
        self.pipe_template = dict.fromkeys(self.pipe_key_types.keys())

    def get_descendants(self, pipe: dict) -> list:
        """List the descendant names of a pipe."""
        descendants = [pipe["name"]]
        if children := pipe.get("children"):
            for child in children:
                descendants.extend(self.get_descendants(child))
        return descendants

    def validate_pipe(self, pipe: dict) -> bool:
        """
        Validate pipeline structure and types.

        - NOTE: Consider using `TypedDict` for type checking instead.
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
        """Create a pipeline from `kwargs`."""
        pipe = self.pipe_template.copy()
        pipe.update(id=str(uuid.uuid4()), name=name, **kwargs)
        return pipe


class PipeTree(Pipe):
    """
    Class for managing pipeline trees.

    Provides methods for creating, searching and analyzing pipeline trees.

    "Pipeline trees" is represented by a list of dictionaries, where each
    dictionary represents a pipeline with its attributes and children.

    The children of a pipeline has the same representation as a a pipeline tree
    (i.e., `list[dict]`). This is a handy feature as it allows functions to
    apply recursively.
    """

    def __init__(self, pipe_tree=None):
        super().__init__()  # Initialize parent class
        self.pipe_tree = pipe_tree
        if pipe_tree is not None:
            # Validate pipeline tree structure
            is_valid = all(self.validate_pipe(pipe) for pipe in pipe_tree)
            if not is_valid:
                raise ValueError("Invalid pipeline tree structure")

            # Create map from IDs to paths
            self.id_path_map = self.create_id_path_map(pipe_tree)

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

    def add_unique_ids(self, pipe_tree: list[dict]) -> None:
        """Add unique IDs to each pipeline in a pipeline tree."""
        for pipe in pipe_tree:
            if not pipe.get("id"):
                pipe["id"] = str(uuid.uuid4())
            if pipe.get("children"):
                self.add_unique_ids(pipe["children"])

    def get_pipe_by_id(self, pipe_tree: list[dict], pipe_id: str) -> dict | None:
        """Get a pipeline by its ID."""
        return next(
            (pipe for pipe in self.search_pipe(pipe_tree, {"id": pipe_id})), None
        )

    def create_id_pipe_map(self, pipe_tree: list[dict]) -> dict:
        """Create a dictionary mapping IDs to pipelines."""
        id_map = {}
        for pipe in pipe_tree:
            if "id" not in pipe:
                raise ValueError("Pipeline missing ID")
            id_map[pipe["id"]] = pipe
            if pipe.get("children"):
                id_map.update(self.create_id_pipe_map(pipe["children"]))
        return id_map

    def create_id_path_map(self, pipe_tree: list[dict], ancestors_path=None) -> dict:
        """Create a dictionary mapping IDs to pipeline paths."""
        id_map: dict[str, list] = {}

        for pipe in pipe_tree:
            # Prevent chaos
            if "id" not in pipe:
                raise KeyError("Pipeline missing ID")

            path = []

            # Add ancestors' path if it exists
            if ancestors_path:
                path.extend(ancestors_path)

            # Add current pipeline to `id_map`
            path.append(pipe["name"])
            id_map[pipe["id"]] = path

            # Recursively run routine on children
            if pipe.get("children"):
                id_map.update(
                    self.create_id_path_map(pipe["children"], ancestors_path=path)
                )

        return id_map

    def _filter_pipetree(self, pipe_tree: list[dict], attrib="name"):
        """
        Filter pipeline tree based on an attribute key.

        The dictionary representing a pipeline with children has the structure
        `{kwargs, children: list}`. The output of this function will return
        `[[val_parent, [[val_child1, [[val_grandchild1, ...]], ...]]]]`.
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

    def write_pipeline(self, pipe_tree: list[dict], path: str):
        """Write pipeline tree to a YAML file."""
        with open(path, "w") as f:
            yaml.dump(pipe_tree, f, sort_keys=False)
