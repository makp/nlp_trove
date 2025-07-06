from collections.abc import Generator

import lxml.etree as ET


class LoadXML:
    def __init__(self, file_paths, id_attrib: None | str = None):
        self.file_paths = file_paths

        # Parse XML files and store their root elements in a dictionary
        self.filepath_to_root: dict[str, ET.Element] = {
            fp: self._return_root(fp) for fp in file_paths
        }

        if id_attrib:
            # Check if the id_attrib is present in all root elements
            elements_sans_id = [
                root
                for root in self.filepath_to_root.values()
                if id_attrib not in root.attrib
            ]
            if elements_sans_id:
                raise ValueError(
                    f"Attribute '{id_attrib}' not found in some root elements"
                )

            # Create a mapping from id to root element
            self.id_to_root = {
                root.attrib[id_attrib]: root for root in self.filepath_to_root.values()
            }

    def _return_root(self, path: str) -> ET.Element:
        """Return the root element of the XML file with the given path."""
        with open(path, "r") as f:
            return ET.parse(f).getroot()


class InspectXML:
    """
    First-order inspection of XML files, including root tags, lengths, and
    namespaces.
    """

    def __init__(self, file_paths):
        intializer = LoadXML(file_paths)
        self.file_paths = file_paths
        self.filepath_to_root = intializer.filepath_to_root

    def _return_root_tags(self):
        """
        Return the tags of the root elements of the XML files.
        """
        return {root.tag for root in self.filepath_to_root.values()}

    def _return_root_lengths(self):
        """
        Return the lengths of the root elements of the XML files.
        """
        return {len(root) for root in self.filepath_to_root.values()}

    def _return_root_common_children(self):
        """
        Return the children of the root elements that are shared across all XML files.
        """
        root_children = (
            {child.tag for child in root} for root in self.filepath_to_root.values()
        )
        return set.intersection(*root_children)

    def check_root(self):
        """
        Check the root elements of the XML files.
        """
        print("\nINFO ABOUT THE ROOT ELEMENTS")
        print("=" * 30)
        print(f"Tags: {self._return_root_tags()}")
        print("-" * 50)
        print(f"Number of children: {self._return_root_lengths()}")
        print("-" * 50)
        print(f"Shared children: {self._return_root_common_children()}")

    def _return_namespaces_from_element(self, element: ET.Element) -> set[tuple]:
        "Return the namespaces within an Element."
        # `.nsmap` returns a dictionary mapping prefixes to URIs.
        # `tuple` is used to transform the ns into hashable tuples.
        return set(ns for el in element.iter("{*}*") for ns in tuple(el.nsmap.items()))

    def _return_namespaces_per_root(self) -> Generator[set[tuple]]:
        "Return generator containing the namespaces for each root element."
        return (
            self._return_namespaces_from_element(root)
            for root in self.filepath_to_root.values()
        )

    def _return_namespaces_all(self) -> set:
        "Return all namespaces."
        return set.union(*self._return_namespaces_per_root())

    def _return_namespaces_shared(self) -> set:
        "Return shared namespaces."
        return set.intersection(*self._return_namespaces_per_root())

    def _return_tags_sans_namespace(self) -> set:
        "Return tags not associated with a namespace."
        return set(
            el.tag for root in self.filepath_to_root.values() for el in root.iter("{}*")
        )

    def check_namespaces(self):
        "Print information about namespaces of the XML files."
        print("\nINFO ABOUT NAMESPACES")
        print("=" * 30)
        print(f"All namespaces: {self._return_namespaces_all()}")
        print("-" * 50)
        print(f"Shared namespaces: {self._return_namespaces_shared()}")
        print("-" * 50)
        print(f"Tags without namespace: {self._return_tags_sans_namespace()}")


# class ProcessXML:
#     def __init__(self):
#         self.map_tags_to_text = {}
#
#     def remove_elements_sans_content(self, element_or_tree, deep=False):
#         """Remove elements in `element_or_tree` that do not contribute with any
#         content (text or tail)."""
#         # Preserve input?
#         if deep:
#             element_or_tree = ET.ElementTree(element_or_tree)
#
#         # Mark elements for removal
#         # Notes:
#         # - `itertext` iterates over the text content of the element and its
#         # descendants, but not the tail of the element.
#         # - Since `itertext` graciously returns an empty string if there is no
#         # content inside the element, `join` won't throw an error if that happens.
#         elements_to_remove = (
#             e
#             for e in element_or_tree.iter()
#             if not ("".join(e.itertext()).strip() + (e.tail or "").strip())
#         )
#
#         # Remove elements
#         for e in elements_to_remove:
#             parent = e.getparent()
#             if parent is not None:
#                 parent.remove(e)
#
#         if deep:
#             return element_or_tree
#
#     def replace_content_from_tags(self, element, deep=False):
#         """Replace the content within certain tags in an Element object."""
#         # Keep input?
#         if deep:
#             element = ET.ElementTree(element)
#
#         # Mark elements that will be replaced
#         elements_to_change = [
#             (e, self.map_tags_to_text[e.tag])
#             for e in element.iter()
#             if e.tag in self.map_tags_to_text
#         ]
#
#         # Replace content
#         for e, new_text in elements_to_change:
#             e.clear(keep_tail=True)  # Clear subelements but keep tail
#             e.text = new_text
#
#         if deep:
#             return element
#
#     def update_map_tags_to_text(self, tag, text):
#         self.map_tags_to_text[tag] = text
#
#     def batch_update_map_tags_to_text(self, tag_text_dict):
#         self.map_tags_to_text.update(tag_text_dict)
