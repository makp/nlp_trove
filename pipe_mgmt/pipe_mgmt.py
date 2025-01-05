PIPE_TEMPLATE = {
    "pipe_name": None,
    "creation_date": None,
    "path": None,
    "parent_pipe": None,
    "children": [],
}


def create_root_pipes(root_pipes: list) -> list[dict]:
    """Create root pipelines."""
    return [{**PIPE_TEMPLATE, "pipe_name": pipe} for pipe in root_pipes]


def find_pipe(pipes: list[dict], conditions: dict) -> list[dict]:
    """Search pipeline recursively for a condition."""
    matches: list = []
    for pipe in pipes:
        if all(pipe.get(key) == value for key, value in conditions.items()):
            matches.append(pipe)
        matches.extend(find_pipe(pipe.get("children", []), conditions))
    return matches


def _get_lineage(root_pipe: dict) -> list[list]:
    """List children from root pipe recursively."""
    children: list[list] = []
    for child in root_pipe.get("children", []):
        children.append([child["pipe_name"]])
        children.extend(_get_lineage(child))
    for lineage in children:
        lineage.insert(0, root_pipe["pipe_name"])
    return children


def list_pipeline_lineage(pipes: list[dict]) -> list[list]:
    """List pipeline lineage."""
    lineages: list = []
    for pipe in pipes:
        pipe_children = _get_lineage(pipe)
        lineages.extend(pipe_children)
    return lineages
