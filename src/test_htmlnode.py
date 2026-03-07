import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("p", "this is a testnode", [], {"color": "Grün", "size": "16px"})
        self.assertEqual(node.__dict__, {
            "tag": "p",
            "value": "this is a testnode",
            "children": [],
            "props": {"color": "Grün", "size": "16px"}
            })

    def test_init_none(self):
        node = HTMLNode()
        self.assertEqual(node.__dict__, {
            "tag": None,
            "value": None,
            "children": None,
            "props": None
            })
        
    def test_to_html(self):
        node = HTMLNode("p", "this is a testnode", [], {"color": "Grün", "size": "16px"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "this is a testnode", [], {})
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_None(self):
        node = HTMLNode("p", "this is a testnode")
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html(self):
        node = HTMLNode("p", "this is a testnode", [], {"color": "green", "size": "16px"})
        expected = " color=\"green\" size=\"16px\""
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_props_as_key(self):
        node = HTMLNode("p", "this is a testnode",  props={"color": "green", "size": "16px"})
        expected = " color=\"green\" size=\"16px\""
        self.assertEqual(node.props_to_html(), expected)

    



class TestLeafNode(unittest.TestCase):

    def test_init(self):
        node = LeafNode("p", "this is a testnode", {"color": "Grün", "size": "16px"})
        self.assertEqual(node.__dict__, {
            "tag": "p",
            "value": "this is a testnode",
            "children": None,
            "props": {"color": "Grün", "size": "16px"}
            })

    def test_init_only_necessary(self):
        node = LeafNode("p", "this is a testnode",)
        self.assertEqual(node.__dict__, {
            "tag": "p",
            "value": "this is a testnode",
            "children": None,
            "props": None
            })
    
    def test_init_not_enough(self):
        with self.assertRaises(TypeError):
            node = LeafNode("p")

    def test_to_html_no_value_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
        
    def test_to_html_no_value_empty(self):
        node = LeafNode("p", "")
        expected = "<p></p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_no_tag_none(self):
        node = LeafNode(None, "This is a paragraph of text.")
        expected = "This is a paragraph of text."
        self.assertEqual(node.to_html(), expected)

    def test_to_html_no_tag_empty(self):
        node = LeafNode("", "This is a paragraph of text.")
        expected = "This is a paragraph of text."
        self.assertEqual(node.to_html(), expected)

    def test_to_html_no_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)

    def props_to_html_not_overwritten(self):
        node = LeafNode("", "This is a paragraph of text.")
        self.assertEqual("props_to_html" in node.__dict__, False)


class testParentNode(unittest.TestCase):

    def test_init(self):
        node = ParentNode("p", [], {"color": "Grün", "size": "16px"})
        self.assertEqual(node.__dict__, {
            "tag": "p",
            "value": None,
            "children": [],
            "props": {"color": "Grün", "size": "16px"}
            })

    def test_init_only_necessary(self):
        node = ParentNode("p", [],)
        self.assertEqual(node.__dict__, {
            "tag": "p",
            "value": None,
            "children": [],
            "props": None
            })
    
    def test_init_not_enough(self):
        with self.assertRaises(TypeError):
            node = ParentNode("p")



    def test_to_html_no_children_none(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
        
    def test_to_html_no_children_empty(self):
        node = ParentNode("p", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag_none(self):
        node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag_empty(self):
        node = ParentNode("", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"size": "15px"}
        )
        expected = "<p size=\"15px\"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_grandchildren(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"size": "15px"}
        )
        node2 = ParentNode(
            "p",
            [
                node
            ]
        )
        expected = "<p><p size=\"15px\"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>"
        self.assertEqual(node2.to_html(), expected)

    def props_to_html_not_overwritten(self):
        node = ParentNode("", "This is a paragraph of text.")
        self.assertEqual("props_to_html" in node.__dict__, False)




if __name__ == "__main__":
    unittest.main()