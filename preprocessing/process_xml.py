import lxml.etree as ET


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
