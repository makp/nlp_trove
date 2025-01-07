class PipeMgmt:
    """
    Class for managing pipelines and their relationships.

    Provides methods for creating, searching and analyzing pipelines.

    The term "pipeline tree" refers a list of dictionaries object, where each
    dictionary represents a pipeline with its attributes and children.
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
