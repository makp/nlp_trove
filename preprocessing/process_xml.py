"""
Classes for inspecting the general structure of XML files (`InspectXML`), and
to search for tags using XPath expressions and text extraction (`SearchXML`).
"""

import os
from collections.abc import Generator

import lxml.etree as ET


class LoadXML:
    def __init__(self, filepaths, id_attrib: None | str = None):
        self.filepaths = filepaths

        # Parse XML files and store their root elements in a dictionary
        self.filepath_to_root: dict[str, ET.Element] = {
            fp: self._return_root(fp) for fp in filepaths
        }

        if id_attrib:
            # Ensure all root elements have the specified attribute
            if any(
                id_attrib not in root.attrib for root in self.filepath_to_root.values()
            ):
                raise ValueError(
                    f"Attribute '{id_attrib}' not found in some root elements"
                )

            # Map id to root element
            self.id_to_root = {
                root.attrib[id_attrib]: root for root in self.filepath_to_root.values()
            }
        else:
            # Use filenames as identifiers if no `id_attrib` is provided
            self.id_to_root = {
                os.path.basename(fp): root for fp, root in self.filepath_to_root.items()
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

    def __init__(self, filepaths):
        initializer = LoadXML(filepaths)
        self.filepaths = filepaths
        self.filepath_to_root = initializer.filepath_to_root

    def _get_root_tags(self):
        """
        Return the tags of the root elements of the XML files.
        """
        return {root.tag for root in self.filepath_to_root.values()}

    def _get_root_child_counts(self):
        """
        Return the number of direct children for each root element.
        """
        return {len(root) for root in self.filepath_to_root.values()}

    def _get_common_child_tags(self):
        """
        Return the child tags that are shared across all root elements.
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
        print(f"Tags: {self._get_root_tags()}")
        print("-" * 50)
        print(f"Number of children: {self._get_root_child_counts()}")
        print("-" * 50)
        print(f"Shared children: {self._get_common_child_tags()}")

    def _get_namespaces_from_element(self, element: ET.Element) -> set[tuple]:
        "Extract all namespaces from an Element and its descendants."
        # `.nsmap` returns a dictionary mapping prefixes to URIs.
        # `tuple` is used to transform the ns into hashable tuples.
        return set(ns for el in element.iter("{*}*") for ns in tuple(el.nsmap.items()))

    def _get_namespaces_per_root(self) -> Generator[set[tuple]]:
        "Generate namespace sets for each root element."
        return (
            self._get_namespaces_from_element(root)
            for root in self.filepath_to_root.values()
        )

    def _get_all_namespaces(self) -> set:
        "Return all unique namespaces found across all XML files."
        return set.union(*self._get_namespaces_per_root())

    def _get_shared_namespaces(self) -> set:
        "Return namespaces that are common to all XML files."
        return set.intersection(*self._get_namespaces_per_root())

    def _get_unnamespaced_tags(self) -> set:
        "Return all tags that are not associated with any namespace."
        return set(
            el.tag for root in self.filepath_to_root.values() for el in root.iter("{}*")
        )

    def check_namespaces(self):
        "Print information about namespaces of the XML files."
        print("\nINFO ABOUT NAMESPACES")
        print("=" * 30)
        print(f"All namespaces: {self._get_all_namespaces()}")
        print("-" * 50)
        print(f"Shared namespaces: {self._get_shared_namespaces()}")
        print("-" * 50)
        print(f"Tags without namespace: {self._get_unnamespaced_tags()}")


class SearchXML:
    """
    Search for specific tags and attributes in XML, and return their text.
    """

    def __init__(
        self,
        filepaths,
        ns: dict | None,
        id_attrib: None | str = None,
    ):
        self.filepaths = filepaths
        loaded_xml = LoadXML(filepaths, id_attrib)
        self.filepath_to_root = loaded_xml.filepath_to_root
        self.id_to_root = loaded_xml.id_to_root
        self.ns = ns if ns else {}

    def find_elements_by_xpath(
        self,
        search_string: str,
    ) -> dict[str, list[ET.Element]]:
        """Map IDs to elements matching the XPath search string."""
        return {
            id: el.xpath(search_string, namespaces=self.ns)
            for id, el in self.id_to_root.items()
        }

    def _group_ids_by_length(self, mapping: dict) -> dict:
        output = {}
        for id, elements in mapping.items():
            key = len(elements)
            if key not in output:
                output[key] = list()
            output[key].append(id)
        return dict(sorted(output.items()))

    def search_and_get_value_counts(self, search_string: str) -> dict:
        """Count occurrences of elements matching the search string."""
        return self._group_ids_by_length(self.find_elements_by_xpath(search_string))

    def _get_text_from_element_recursive(self, element, with_tail=True):
        """
        Get text from an XML element recursively.

        If `with_tail` is True, include the tail text of the element (text that
        appears after the element's closing tag but before the next sibling
        element)
        """
        main_text = " ".join(element.itertext()).strip()
        if with_tail and element.tail:
            main_text = f"{main_text} {element.tail.strip()}"
        return main_text

    def search_and_get_text_recursive(
        self,
        search_str: str,
        join_str: str | None = None,
        with_tail: bool = True,
    ) -> dict[str, str | list[str]]:
        """
        Search for elements matching the search string and return their text.

        Args:
            search_str: XPath expression to search for elements
            join_str: String to join matched element texts. If None, returns list of texts
            with_tail: Whether to include tail text from matched elements

        Returns:
            Dictionary mapping element IDs to either joined text (if join_str provided)
            or list of text strings (if join_str is None)
        """
        assert join_str is None or isinstance(join_str, str), (
            "join_str must be a string or None"
        )

        result = {}

        # XPath search results
        id_to_elements: dict[str, list] = self.find_elements_by_xpath(search_str)

        for id, elements in id_to_elements.items():
            if not elements:  # Handle empty search results
                result[id] = "" if join_str is not None else []
                continue

            texts = [
                self._get_text_from_element_recursive(el, with_tail) for el in elements
            ]

            if join_str is None:
                result[id] = texts
            else:
                result[id] = join_str.join(texts).strip()

        return result

    def search_and_get_attrib_and_text(
        self,
        search_str: str,
        attrib: str,
    ) -> dict[str, list[tuple]]:
        """
        Search for elements matching the search string and return their attributes
        and text as a list of tuples.
        """
        result = {}

        # XPath search results
        id_to_elements: dict[str, list] = self.find_elements_by_xpath(search_str)

        for id, elements in id_to_elements.items():
            if not elements:  # Handle empty search results
                result[id] = []
                continue

            result[id] = [
                (el.attrib.get(attrib, ""), el.text.strip()) for el in elements
            ]

        return result

    def print_tails(self, search_str: str):
        """Search for tail text in elements matching the search string."""
        for id, elements in self.find_elements_by_xpath(search_str).items():
            tails = [el.tail.strip() for el in elements if el.tail and el.tail.strip()]
            if tails:
                print(f"Element with id {id} has tail text: {', '.join(tails)}")


# class EditXML:
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
