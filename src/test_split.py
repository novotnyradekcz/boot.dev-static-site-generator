import unittest

from split import split_nodes_delimiter, split_nodes_image, split_nodes_link
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
            TextNode("This is just text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, actual_nodes)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_more_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png), and the same one again: ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        text_node = TextNode("This is just text", TextType.TEXT)
        new_nodes = split_nodes_image([node, text_node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(", and the same one again: ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is just text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com/) and another [second link](https://www.example.com/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com/"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.example.com/"),
            ],
            new_nodes,
        )

    def test_split_more_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com/) and another [second link](https://www.example.com/), and once more: [second link](https://www.example.com/).",
            TextType.TEXT,
        )
        text_node = TextNode("This is just text", TextType.TEXT)
        new_nodes = split_nodes_link([text_node, node, text_node])
        self.assertListEqual(
            [
                TextNode("This is just text", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com/"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.example.com/"),
                TextNode(", and once more: ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.example.com/"),
                TextNode(".", TextType.TEXT),
                TextNode("This is just text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_one_link(self):
        node = TextNode(
            "[link](https://example.com/)",
            TextType.TEXT,
        )
        text_node = TextNode("This is just text", TextType.TEXT)
        new_nodes = split_nodes_link([text_node, node, text_node])
        self.assertListEqual(
            [
                TextNode("This is just text", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com/"),
                TextNode("This is just text", TextType.TEXT)
            ],
            new_nodes,
        )
