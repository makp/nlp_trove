import lxml.etree as ET


class InspectXML:
    """
    First-order inspection of XML files, including root tags, lengths, and
    namespaces.
    """

    def __init__(self, file_paths: list[str]):
        self.file_paths = file_paths

    def _return_root(self, path: str) -> ET.Element:
        """Return the root element of the XML file with the given path."""
        with open(path, "r") as f:
            return ET.parse(f).getroot()

    def _return_root_tags(self):
        """
        Return the tags of the root elements of the XML files.
        """
        root_tags = {self._return_root(filename).tag for filename in self.file_paths}
        return root_tags

    def _return_root_lengths(self):
        """
        Return the lengths of the root elements of the XML files.
        """
        root_lengths = {
            len(self._return_root(filename)) for filename in self.file_paths
        }
        return root_lengths

    def check_root(self):
        """
        Check the root elements of the XML files.
        """
        root_tags = self._return_root_tags()
        root_lengths = self._return_root_lengths()

        print(f"Root tags: {root_tags}")
        print("-" * 50)
        print(f"Root lengths: {root_lengths}")

    def _return_root_namespaces(self):
        """
        Return the namespaces of the root element of the XML files.
        """
        all_namespaces = set()
        for filename in self.file_paths:
            root = self._return_root(filename)
            all_namespaces.update(set(root.nsmap.items()))
        return all_namespaces

    def _return_all_namespaces(self):
        """
        Search for all namespaces in the XML files and return a set of their
        keys and values.
        """
        all_namespaces = set()
        for filename in self.file_paths:
            root = self._return_root(filename)
            for el in root.iter("{*}*"):
                all_namespaces.update(set(el.nsmap.items()))
        return all_namespaces

    def _return_elements_sans_namespace(self):
        """
        Return elements in the XML files without namespace.
        """
        elements_sans_namespace = set()
        for filename in self.file_paths:
            root = self._return_root(filename)
            tags_sans_namespace = {el.tag for el in root.iter("{}*")}
            elements_sans_namespace.update(tags_sans_namespace)
        return elements_sans_namespace

    def check_namespaces(self):
        """
        Check if the XML files have namespaces.
        """
        root_namespaces = self._return_root_namespaces()
        all_namespaces = self._return_all_namespaces()
        elements_sans_namespace = self._return_elements_sans_namespace()

        print(f"Root namespaces: {root_namespaces}")
        print("-" * 50)
        print(f"All namespaces: {all_namespaces}")
        print("-" * 50)
        print(f"Tags without namespace: {elements_sans_namespace}")


class ProcessXML:
    def __init__(self):
        self.map_tags_to_text = {}

    def remove_elements_sans_content(self, element_or_tree, deep=False):
        """Remove elements in `element_or_tree` that do not contribute with any
        content (text or tail)."""
        # Preserve input?
        if deep:
            element_or_tree = ET.ElementTree(element_or_tree)

        # Mark elements for removal
        # Notes:
        # - `itertext` iterates over the text content of the element and its
        # descendants, but not the tail of the element.
        # - Since `itertext` graciously returns an empty string if there is no
        # content inside the element, `join` won't throw an error if that happens.
        elements_to_remove = (
            e
            for e in element_or_tree.iter()
            if not ("".join(e.itertext()).strip() + (e.tail or "").strip())
        )

        # Remove elements
        for e in elements_to_remove:
            parent = e.getparent()
            if parent is not None:
                parent.remove(e)

        if deep:
            return element_or_tree

    def replace_content_from_tags(self, element, deep=False):
        """Replace the content within certain tags in an Element object."""
        # Keep input?
        if deep:
            element = ET.ElementTree(element)

        # Mark elements that will be replaced
        elements_to_change = [
            (e, self.map_tags_to_text[e.tag])
            for e in element.iter()
            if e.tag in self.map_tags_to_text
        ]

        # Replace content
        for e, new_text in elements_to_change:
            e.clear(keep_tail=True)  # Clear subelements but keep tail
            e.text = new_text

        if deep:
            return element

    def update_map_tags_to_text(self, tag, text):
        self.map_tags_to_text[tag] = text

    def batch_update_map_tags_to_text(self, tag_text_dict):
        self.map_tags_to_text.update(tag_text_dict)
