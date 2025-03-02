import os
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
        "tree_path": None | str,
        "files": None | dict,
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

    def create_pipe(self, **kwargs) -> dict:
        """Create a pipeline from `kwargs`."""
        pipe = self.pipe_template.copy()
        pipe.update(id=str(uuid.uuid4()), **kwargs)
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

    def __init__(self, pipe_tree=None, validate=True):
        super().__init__()  # Initialize parent class
        # Check if `pipe_tree` is a file path
        if pipe_tree and not isinstance(pipe_tree, list):
            if os.path.exists(pipe_tree) and pipe_tree.endswith(".yaml"):
                with open(pipe_tree, "r") as f:
                    pipe_tree = yaml.safe_load(f)

        self.pipe_tree = pipe_tree or []

        if pipe_tree:
            # Create map from IDs to tree paths
            self.id_path_map = {}
            for id, lst in self.create_id_path_map(pipe_tree).items():
                self.id_path_map[id] = "_".join(lst)

            if validate:
                is_valid = all(self.validate_pipe(pipe) for pipe in pipe_tree)
                if not is_valid:
                    raise ValueError("Invalid pipeline tree structure")

    def create_pipe_tree(self, lst_args: list[dict], validate: bool) -> list[dict]:
        """Create a pipeline tree from a list of dictionaries containing the pipeline attributes."""
        pipe_tree = [self.create_pipe(**kwargs) for kwargs in lst_args]
        if validate:
            if not all(self.validate_pipe(pipe) for pipe in pipe_tree):
                raise ValueError("Invalid pipeline tree structure")
        return pipe_tree

    def get_terminal_pipes(self, pipe_tree=None) -> list[dict]:
        """Get terminal pipelines from a pipeline tree."""
        # Use instance variable if `pipe_tree` not provided
        pipe_tree = pipe_tree or self.pipe_tree

        terminals = []
        for pipe in pipe_tree:
            if pipe.get("children"):
                terminals.extend(self.get_terminal_pipes(pipe["children"]))
            else:
                terminals.append(pipe)
        return terminals

    def _map_levels_to_ids(self) -> dict:
        """
        Map pipeline paths to their nested level.

        The root pipelines are at level 0, their children at level 1, and so on.
        """
        id_level_map = {k: len(v.split("_")) - 1 for k, v in self.id_path_map.items()}

        level_id_map = {k: [] for k in set(id_level_map.values())}
        for k, v in id_level_map.items():
            level_id_map[v].append(k)

        return level_id_map

    def get_pipes_from_level(self, level: int) -> list[dict]:
        """Get pipelines from a specific level."""
        # Map levels to list of IDs
        level_id_map = self._map_levels_to_ids()

        # Allow for negative indexing
        selected_level = tuple(level_id_map.keys())[level]

        # Search for pipelines with the selected level
        lst_ids = level_id_map[selected_level]
        lst_out = []
        for id in lst_ids:
            lst_out.append(self.get_pipe_by_id(pipe_id=id, pipe_tree=self.pipe_tree))

        return lst_out

    def search_pipe(self, conditions: dict, pipe_tree=None) -> list[dict]:
        """Search for a pipe that matches conditions."""
        pipe_tree = pipe_tree or self.pipe_tree

        matches = []

        for pipe in pipe_tree:
            if all(pipe.get(key, None) == value for key, value in conditions.items()):
                matches.append(pipe)
            else:
                if pipe.get("children"):
                    matches.extend(self.search_pipe(conditions, pipe["children"]))
        return matches

    def add_unique_ids(self, pipe_tree: list[dict]) -> None:
        """Add unique IDs to each pipeline in a pipeline tree."""
        for pipe in pipe_tree:
            if not pipe.get("id"):
                pipe["id"] = str(uuid.uuid4())
            if pipe.get("children"):
                self.add_unique_ids(pipe["children"])

    def get_pipe_by_id(
        self,
        pipe_id: str,
        pipe_tree: list[dict] | None = None,
    ) -> dict | None:
        """Get a pipeline by its ID."""
        pipe_tree = pipe_tree or self.pipe_tree
        return next(
            (pipe for pipe in self.search_pipe({"id": pipe_id}, pipe_tree)), None
        )

    def create_id_pipe_map(self, pipe_tree: list[dict]) -> dict:
        """Create a dictionary that maps IDs to pipelines."""
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
            path.append(pipe["shortname"] or pipe["name"])
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

    def list_paths(self, pipe_tree: list[dict], attrib="name"):
        """List all pipeline paths."""
        filtered_tree = self._filter_pipetree(pipe_tree, attrib)
        return self._flatten_filtered_pipetree(filtered_tree)

    def assign_children(
        self,
        func,
        pipe_tree=None,
        validate=True,
    ) -> None:
        """Write children to a pipeline tree and populate their ids."""
        pipe_tree = pipe_tree or self.pipe_tree

        for pipe in pipe_tree:
            children_kwargs = func(pipe)
            children = self.create_pipe_tree([children_kwargs], validate)
            pipe["children"].extend(children)

    def write_pipe_tree(
        self,
        pipe_tree=None,
        path: str = "pipelines.yaml",
    ) -> None:
        """Write pipeline tree to a YAML file."""
        pipe_tree = pipe_tree or self.pipe_tree
        with open(path, "w") as f:
            yaml.dump(pipe_tree, f, sort_keys=False)
