import unittest

from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a diferent text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_all_eq(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.example.com/")
        node2 = TextNode("This is a link node", TextType.LINK, "https://www.example.com/")
        self.assertEqual(node, node2)

    def test_link_img_not_eq(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.example.com/")
        node2 = TextNode("This is a link node", TextType.IMAGE, "https://www.example.com/")
        self.assertNotEqual(node, node2)

    def test_text_type_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic_text(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_link_text(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://www.example.com/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "https://www.example.com/"})

    def test_image_text(self):
         node = TextNode("This is an image", TextType.IMAGE, "https://www.example.com/image.png")
         html_node = text_node_to_html_node(node)
         self.assertEqual(html_node.tag, "img")
         self.assertEqual(html_node.value, "")
         self.assertEqual(html_node.props, {"src": "https://www.example.com/image.png", "alt": "This is an image"})

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![cool image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("cool image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [interesting link](https://www.example.com/)"
        )
        self.assertListEqual([("interesting link", "https://www.example.com/")], matches)



if __name__ == "__main__":
    _ = unittest.main()
