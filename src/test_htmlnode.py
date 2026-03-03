import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("p", "this is a testnode", [], {"color": "Grün", "size": "16px"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.__dict__, {
            "tag": None,
            "value": None,
            "children": None,
            "props": None
            })

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "this is a testnode", [], {})
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_None(self):
        node = HTMLNode("p", "this is a testnode")
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_props_as_key(self):
        node = HTMLNode("p", "this is a testnode",  props={"color": "green", "size": "16px"})
        expected = " color=green size=16px"
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html(self):
        node = HTMLNode("p", "this is a testnode", [], {"color": "green", "size": "16px"})
        expected = " color=green size=16px"
        self.assertEqual(node.props_to_html(), expected)


if __name__ == "__main__":
    unittest.main()