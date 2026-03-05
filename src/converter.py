from textnode import *
from htmlnode import *


def text_node_to_html_node(textnode):
    match textnode.text_type:
        case TextType.TEXT:
            return LeafNode(None, textnode.text)
        case TextType.BOLD:
            return LeafNode("b", textnode.text)
        case TextType.ITALIC:
            return LeafNode("i", textnode.text)
        case TextType.CODE:
            return LeafNode("code", textnode.text)
        case TextType.LINK:
            return LeafNode("link", textnode.text, props = {"href": textnode.url})
        case TextType.IMAGE:
            return LeafNode("img", "", props = {"src": textnode.url, "alt": textnode.text})
        case _:
            raise Exception