class PipeMgmt:
    """
    Class for managing pipelines and their relationships.

    Provides methods for creating, searching and analyzing pipelines.
    """

    def __init__(self):
        self.pipe_template = {
            "pipe_name": None,
            "creation_date": None,
            "path": None,
            "parent_pipe": None,
            "children": [],
        }

    def create_root_pipes(self, root_pipes: list) -> list[dict]:
        """Create root pipelines."""
        return [{**self.pipe_template, "pipe_name": pipe} for pipe in root_pipes]

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
            children.append([child["pipe_name"]])
            children.extend(self.get_lineage(child))
        for lineage in children:
            lineage.insert(0, root_pipe["pipe_name"])
        return children

    def list_lineages(self, pipes: list[dict]) -> list[list]:
        """List pipeline lineage."""
        lineages = []
        for pipe in pipes:
            pipe_children = self.get_lineage(pipe)
            lineages.extend(pipe_children)
        return lineages
