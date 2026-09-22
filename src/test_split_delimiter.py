import unittest

from split_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        actual_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, actual_nodes)

    def test_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        text_node = TextNode("This is just text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, text_node], "**", TextType.BOLD)
        actual_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            TextNode("This is just text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, actual_nodes)

    def test_italic(self):
        node = TextNode("This is text with a word in _italics_", TextType.TEXT)
        text_node = TextNode("This is just text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, text_node], "_", TextType.ITALIC)
        actual_nodes = [
            TextNode("This is text with a word in ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC),
            TextNode("", TextType.TEXT),
            TextNode("This is just text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, actual_nodes)
