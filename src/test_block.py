import unittest

from block import BlockType, block_to_block_type, markdown_to_blocks


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_with_empty_lines_to_blocks(self):
        md = """


This is **bolded** paragraph




        This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_headings_block_to_blocktype(self):
        h1 = "# This is a heading."
        h3 = "### This is also a heading."
        h6 = "###### Even this is a heading."
        self.assertEqual(block_to_block_type(h1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(h3), BlockType.HEADING)
        self.assertEqual(block_to_block_type(h6), BlockType.HEADING)

    def test_code_block_to_blocktype(self):
        code = """```
x = "Bob"
if x == "Bob":
    print("Hello, Bob!")
else:
    print("Hello, stranger.")
```"""
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_quote_block_to_blocktype(self):
        quote = """> This is
>a
> very insightful quote."""
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

    def test_unordered_list_block_to_blocktype(self):
        unordered_list = """- Item one
- Item three
- Item two
- Very unordered!"""
        self.assertEqual(block_to_block_type(unordered_list), BlockType.UNORDERED_LIST)

    def test_ordered_list_block_to_blocktype(self):
        ordered_list = """1. Item one
2. Item two
3. Item three
4. Very ordered!"""
        self.assertEqual(block_to_block_type(ordered_list), BlockType.ORDERED_LIST)

    def test_wrong_ordered_list_block_to_blocktype(self):
        ordered_list = """1. Wrongly ordered list
3. is just a paragraph"""
        self.assertEqual(block_to_block_type(ordered_list), BlockType.PARAGRAPH)

    def test_paragraph_block_to_blocktype(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
