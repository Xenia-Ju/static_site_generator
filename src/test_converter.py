import unittest

from textnode import *
from htmlnode import *
from converter import *

class test_text_node_to_html(unittest.TestCase):
    def test_text_to_html_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        expected = {"tag": None, "value": "This is a text node", "children": None,"props": None }
        self.assertEqual(html_node.__dict__, expected)

    def test_text_to_html_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        expected = {"tag": "b", "value": "This is a text node", "children": None,"props": None }
        self.assertEqual(html_node.__dict__, expected)

    def test_text_to_html_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        expected = {"tag": "i", "value": "This is a text node", "children": None,"props": None }
        self.assertEqual(html_node.__dict__, expected)

    def test_text_to_html_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        expected = {"tag": "code", "value": "This is a text node", "children": None,"props": None }
        self.assertEqual(html_node.__dict__, expected)

    def test_text_to_html_link(self):
        node = TextNode("This îs a link", TextType.LINK, "HTTP")
        html_node = text_node_to_html_node(node)
        expected = {"tag": "link", "value": "This îs a link", "children": None,"props": {"href": "HTTP"} }
        self.assertEqual(html_node.__dict__, expected)

    def test_text_to_html_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "IMAGELOCATION")
        html_node = text_node_to_html_node(node)
        expected = {"tag": "img", "value": "", "children": None,"props": {"src": "IMAGELOCATION", "alt": "This is an image"} }
        self.assertEqual(html_node.__dict__, expected)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node.text_type = "Wrong"
        with self.assertRaises(Exception):
            html_node = text_node_to_html_node(node)




if __name__ == "__main__":
    unittest.main()