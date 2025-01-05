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


def find_pipe(pipes: list[dict], pipe_name: str) -> list[dict]:
    """Search pipeline recursively."""
    lst_matches = []
    for pipe in pipes:
        if pipe["pipe_name"] == pipe_name:
            lst_matches.append(pipe)
        lst_matches.extend(find_pipe(pipe.get("children", []), pipe_name))
    return lst_matches


def _list_pipe_lineage(root_pipe: dict) -> list[list]:
    """List children from root pipe recursively."""
    lst_children: list[list] = []
    for child in root_pipe.get("children", []):
        lst_children.append([child["pipe_name"]])
        lst_children.extend(_list_pipe_lineage(child))
    for lineage in lst_children:
        lineage.insert(0, root_pipe["pipe_name"])
    return lst_children


def list_pipeline_lineage(pipes: list[dict]) -> list[list]:
    """List pipeline lineage."""
    lst_lineage = []
    for pipe in pipes:
        pipe_children = _list_pipe_lineage(pipe)
        lst_lineage.extend(pipe_children)
    return lst_lineage

