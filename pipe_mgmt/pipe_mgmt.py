class PipeMgmt:
    """
    Class for managing pipelines and their relationships.

    Provides methods for creating, searching and analyzing pipelines.
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

    def __init__(self):
        self.pipe_template = dict.fromkeys(self.pipe_key_types.keys())

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

    def find_pipe(self, pipes: list[dict], conditions: dict) -> list[dict]:
        """Search pipeline recursively for a condition."""
        matches = []
        for pipe in pipes:
            if all(pipe.get(key) == value for key, value in conditions.items()):
                matches.append(pipe)
            matches.extend(self.find_pipe(pipe.get("children", []), conditions))
        return matches

    def get_lineage(self, root_pipe: dict) -> list[list]:
        """List children from root pipe recursively."""
        children: list[list] = []
        for child in root_pipe.get("children", []):
            children.append([child["name"]])
            children.extend(self.get_lineage(child))
        for lineage in children:
            lineage.insert(0, root_pipe["name"])
        return children

    def list_lineages(self, pipes: list[dict]) -> list[list]:
        """List pipeline lineage."""
        lineages = []
        for pipe in pipes:
            pipe_children = self.get_lineage(pipe)
            lineages.extend(pipe_children)
        return lineages
