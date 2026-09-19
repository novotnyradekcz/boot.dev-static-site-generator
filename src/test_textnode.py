import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    _ = unittest.main()
