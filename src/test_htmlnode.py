import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "This is a link node", [HTMLNode(), HTMLNode()], {"href": "https://www.example.com/"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com/"')

    def test_multiple_props_to_html(self):
        node = HTMLNode("a", "This is a link node", props={"href": "https://www.example.com/", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com/" target="_blank"')


if __name__ == "__main__":
    _ = unittest.main()
