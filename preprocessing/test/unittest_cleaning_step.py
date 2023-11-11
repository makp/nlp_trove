"""Test the clean_text function."""

import unittest
from parameterized import parameterized
from preprocessing.clean_text import TextCleaner


TEXT = """
• Item one is the first bullet point
This is a hyphen­ated word split by an incon-
venient line-break.
She said, “Testing is crucial,” and he replied, ‘Absolutely!’
The café's vintage sign cost ₽5,000. Check out the details at
our-website.com or www.our-website.com or contact us at
info@example.com. For inquiries, call +1 (555) 123-4567.
"""

# Initialize the TextCleaner class
tc = TextCleaner()


class TestCleanText(unittest.TestCase):
    """Use unittest to test cleaning routines."""

    @parameterized.expand([
        ("hyphen-break",
         "incon-\nvenient line-break.",
         "inconvenient line-break."),
        ("normalize-quotes",
         'She said, “Testing is crucial,”',
         'She said, "Testing is crucial,"'),])
    def test_normalization(self, name, raw_text, expected_text):
        """Test normalization steps."""
        self.assertEqual(tc.normalize_text(raw_text),
                         expected_text)

    def setUp(self):
        """Set up the test."""
        self.processed_text = tc.clean_text(TEXT)

    def test_text_elements(self):
        """Check whether text elements (e.g., URLs) were removed."""
        self.assertNotIn("www.our-website.com", self.processed_text)
        self.assertNotIn("info@example.com", self.processed_text)
        self.assertNotIn("₽5,000", self.processed_text)
        self.assertNotIn("+1 (555) 123-4567", self.processed_text)

    def test_punctuation(self):
        """Check whether punctuations were removed."""
        self.assertNotIn("•", self.processed_text)
        self.assertNotIn("“", self.processed_text)
        self.assertNotIn("‘", self.processed_text)
        self.assertNotIn("'", self.processed_text)
        self.assertNotIn(",", self.processed_text)
        self.assertNotIn("é", self.processed_text)


if __name__ == '__main__':
    unittest.main()
