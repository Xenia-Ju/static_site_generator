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



class test_split_nodes_delimiter(unittest.TestCase):

    def test_no_text(self):
        node_2 = TextNode("This is a test node Bold", TextType.BOLD)
        node_3 = TextNode("This is a test node Italic", TextType.ITALIC)
        self.assertEqual(split_nodes_delimiter([node_2, node_3,], "**", TextType.BOLD),
                         [node_2, node_3])
    
    def test_only_final_nodes(self):
        node_1 = TextNode("This is a test node text", TextType.TEXT)
        node_2 = TextNode("This is a test node Bold", TextType.BOLD)
        node_3 = TextNode("This is a test node Italic", TextType.ITALIC)
        self.assertEqual(split_nodes_delimiter([node_1, node_2, node_3,], "**", TextType.BOLD),
                         [node_1, node_2, node_3])

    def test_only_split_bold(self):
        node_1 = TextNode("This is a test node text", TextType.TEXT)
        node_2 = TextNode("This is a test node Bold", TextType.BOLD)
        node_3 = TextNode("This is a test node Italic", TextType.ITALIC)
        node_4 = TextNode("This **Node** should be **split**.", TextType.TEXT)
        expected = [node_1, node_2, node_3,
                    TextNode("This ", TextType.TEXT),
                    TextNode("Node", TextType.BOLD),
                    TextNode(" should be ", TextType.TEXT),
                    TextNode("split", TextType.BOLD),
                    TextNode(".", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter([node_1, node_2, node_3, node_4], "**", TextType.BOLD),
                         expected)
        
    def test_only_split_italic(self):
        node_1 = TextNode("This is a test node text", TextType.TEXT)
        node_2 = TextNode("This is a test node Bold", TextType.BOLD)
        node_3 = TextNode("This is a test node Italic", TextType.ITALIC)
        node_4 = TextNode("This _Node_ should be _split_.", TextType.TEXT)
        expected = [node_1, node_2, node_3,
                    TextNode("This ", TextType.TEXT),
                    TextNode("Node", TextType.ITALIC),
                    TextNode(" should be ", TextType.TEXT),
                    TextNode("split", TextType.ITALIC),
                    TextNode(".", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter([node_1, node_2, node_3, node_4], "_", TextType.ITALIC),
                         expected)
        
    def test_only_split_code(self):
        node_1 = TextNode("This is a test node text", TextType.TEXT)
        node_2 = TextNode("This is a test node Bold", TextType.BOLD)
        node_3 = TextNode("This is a test node Italic", TextType.ITALIC)
        node_4 = TextNode("This `Node` should be `split`.", TextType.TEXT)
        expected = [node_1, node_2, node_3,
                    TextNode("This ", TextType.TEXT),
                    TextNode("Node", TextType.CODE),
                    TextNode(" should be ", TextType.TEXT),
                    TextNode("split", TextType.CODE),
                    TextNode(".", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter([node_1, node_2, node_3, node_4], "`", TextType.CODE),
                         expected)

    def test_split_bold_and_italic(self):
        node_1 = TextNode("This is a test node text", TextType.TEXT)
        node_2 = TextNode("This is a test node Bold", TextType.BOLD)
        node_3 = TextNode("This is a test node Italic", TextType.ITALIC)
        node_4 = TextNode("This **Node** should be _split_", TextType.TEXT)
        expected = [node_1, node_2, node_3,
                    TextNode("This ", TextType.TEXT),
                    TextNode("Node", TextType.BOLD),
                    TextNode(" should be ", TextType.TEXT),
                    TextNode("split", TextType.ITALIC),
                    TextNode("", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter(split_nodes_delimiter([node_1, node_2, node_3, node_4], "**", TextType.BOLD), "_", TextType.ITALIC),
                         expected)
    

    def test_only_split_bold_and_bold_at_end(self):
        node_1 = TextNode("This is a test node text", TextType.TEXT)
        node_2 = TextNode("This is a test node Bold", TextType.BOLD)
        node_3 = TextNode("This is a test node Italic", TextType.ITALIC)
        node_4 = TextNode("This **Node** should be **split**", TextType.TEXT)
        expected = [node_1, node_2, node_3,
                    TextNode("This ", TextType.TEXT),
                    TextNode("Node", TextType.BOLD),
                    TextNode(" should be ", TextType.TEXT),
                    TextNode("split", TextType.BOLD),
                    TextNode("", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter([node_1, node_2, node_3, node_4], "**", TextType.BOLD),
                         expected)

class test_extract_markdown_images(unittest.TestCase):

    def test_extract_two_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_contains_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

class test_extract_markdown_links(unittest.TestCase):

    def test_extract_two_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_contains_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

class text_split_nodes_image(unittest.TestCase):

    def test_no_text_node(self):
        node_1 = TextNode("This is a test node Bold", TextType.BOLD)
        node_2 = TextNode("This is a test node Italic", TextType.ITALIC)
        self.assertEqual(split_nodes_image([node_1, node_2,]),
                         [node_1, node_2])

    def test_no_image(self):
        node_1 = TextNode("This is a test node Bold", TextType.BOLD)
        node_2 = TextNode("This is a test node Italic", TextType.ITALIC)
        node_3 = TextNode("This is a just text", TextType.TEXT)
        self.assertEqual(split_nodes_image([node_1, node_2, node_3]),
                         [node_1, node_2, node_3])

    def test_only_image(self):
        node_1 = TextNode("This is a test node Bold", TextType.BOLD)
        node_2 = TextNode("This is a test node Italic", TextType.ITALIC)
        node_3 = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        expected = [node_1, node_2, TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif" )]
        self.assertEqual(split_nodes_image([node_1, node_2, node_3]), expected)

    def test_images_with_text_around(self):
        node_1 = TextNode("This is a test node Bold", TextType.BOLD)
        node_2 = TextNode("This is a test node Italic", TextType.ITALIC)
        node_3 = TextNode("these images ![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) are classics.", TextType.TEXT)
        expected = [node_1, node_2, 
                    TextNode("these images ", TextType.TEXT),
                    TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" are classics.", TextType.TEXT)]
        self.assertEqual(split_nodes_image([node_1, node_2, node_3]), expected)


class text_split_nodes_links(unittest.TestCase):

    def test_no_text_node(self):
        node_1 = TextNode("This is a test node Bold", TextType.BOLD)
        node_2 = TextNode("This is a test node Italic", TextType.ITALIC)
        self.assertEqual(split_nodes_link([node_1, node_2,]),
                         [node_1, node_2])

    def test_no_image(self):
        node_1 = TextNode("This is a test node Bold", TextType.BOLD)
        node_2 = TextNode("This is a test node Italic", TextType.ITALIC)
        node_3 = TextNode("This is a just text", TextType.TEXT)
        self.assertEqual(split_nodes_link([node_1, node_2, node_3]),
                         [node_1, node_2, node_3])

    def test_only_link(self):
        node_1 = TextNode("This is a test node Bold", TextType.BOLD)
        node_2 = TextNode("This is a test node Italic", TextType.ITALIC)
        node_3 = TextNode("[to boot dev](https://www.boot.dev)", TextType.TEXT)
        expected = [node_1, node_2, TextNode("to boot dev", TextType.LINK, "https://www.boot.dev" )]
        self.assertEqual(split_nodes_link([node_1, node_2, node_3]), expected)

    def test_links_with_text_around(self):
        node_1 = TextNode("This is a test node Bold", TextType.BOLD)
        node_2 = TextNode("This is a test node Italic", TextType.ITALIC)
        node_3 = TextNode("these links [to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev) are good tests.", TextType.TEXT)
        expected = [node_1, node_2, 
                    TextNode("these links ", TextType.TEXT),
                    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                    TextNode(" are good tests.", TextType.TEXT)]
        self.assertEqual(split_nodes_link([node_1, node_2, node_3]), expected)

class test_text_to_textnodes(unittest.TestCase):

    def test_empty_text(self):
        text = ""
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_find_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
                        TextNode("This is ", TextType.TEXT),
                        TextNode("text", TextType.BOLD),
                        TextNode(" with an ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word and a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" and an ", TextType.TEXT),
                        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ", TextType.TEXT),
                        TextNode("link", TextType.LINK, "https://boot.dev"),
                    ]
        self.assertEqual(text_to_textnodes(text), expected)


if __name__ == "__main__":
    unittest.main()