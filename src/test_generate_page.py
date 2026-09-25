import unittest

from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        markdown = """# Page title"""
        self.assertEqual(extract_title(markdown), "Page title")

    def test_extract_title_from_page(self):
        markdown = """
# Page title

## Subtitle

This is some page content.

- And here is a short list"""
        self.assertEqual(extract_title(markdown), "Page title")

    def test_extract_title_hidden(self):
        markdown = """
## This is not the title title

## Subtitle

This is some page content.

- And here is a short list

# Hidden title

More content."""
        self.assertEqual(extract_title(markdown), "Hidden title")
