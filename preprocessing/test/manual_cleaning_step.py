"""Manual test for cleaning_step.py."""

from preprocessing.test.unittest_cleaning_step import TEXT
from preprocessing.clean_text import TextCleaner


# Initialize the TextCleaner class
tc = TextCleaner()


# Section
# -------
# Test general cleaning steps

def manual_test():
    """Inspect the cleaning steps."""
    norm_text = tc.normalize_text(TEXT)
    repl_text = tc.replace_from_text(norm_text)

    print(f"""Original text:{TEXT}
    Normalized:{norm_text}
    Without textual elements:{repl_text}
    Final:{tc.clean_text(TEXT)}""")


# Manual test
manual_test()


# Section
# -------
# Test HTML cleaning steps

html_1 = """
<!DOCTYPE html>
<html>
<head>
    <title>Philosophy of Biology</title>
    <style>
        .important { color: #336699; }
    </style>
</head>
<body>
    <!-- This is a comment that should be removed -->
    <h1>Biology and Philosophy: An Introduction</h1><p>
Understanding the
<strong>philosophy</strong> of biology can
    enrich the way we study and perceive life.</p>
    <p class="important">&copy; 2023 Philosophy Studies</p>
    <script type="text/javascript">
        // This script does something unnecessary
        console.log("Hello World!");
    </script>
</body>
</html>
"""

html_2 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,
    initial-scale=1.0">
    <title>Biological Theories</title>
    <!-- Styles should be removed -->
    <style type="text/css">
        body { font-family: Arial, sans-serif; }
    </style>
</head>
<body>
    <!-- Page comment -->
    <h2>Evolutionary Principles</h2>
    <p>The principle of natural selection is central to understanding
    evolution.
    How does the cleaning step handle hyphenated words: Long-term
    processes.</p>
    <a href="http://example.com" target="_blank">Learn more</a>
    <footer>
        <p>Contact: <a
        href="mailto:info@biology-philosophy.com">info@biology-philosophy.com</a></p>
    </footer>
    <!-- Scripts are not needed in the output text -->
    <script>
        alert("This should not appear in the output");
    </script>
</body>
</html>
"""

print(tc.clean_html(html_1))
print(tc.clean_html(html_2))
