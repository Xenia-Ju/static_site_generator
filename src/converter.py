from textnode import *
from htmlnode import *
import re


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
        

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        seperated_nodes = old_node.text.split(delimiter)
        if len(seperated_nodes) %2 == 0:
            raise Exception(f"That's invalid Markdown syntax. Closing {delimiter} missing.")
        for count, new_node in enumerate(seperated_nodes):
            if count %2 == 0:
                new_nodes.append(TextNode(new_node, TextType.TEXT))
            else:
                new_nodes.append(TextNode(new_node, text_type))
    return new_nodes

def extract_markdown_images(text):
    images = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return links

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        extracted_images = extract_markdown_images(old_node.text)
        if len(extracted_images) == 0:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        for alt, path in extracted_images:
            mk_text = f"![{alt}]({path})"
            pos = text.index(mk_text)
            if pos != 0:
                new_nodes.append(TextNode(text[0:pos], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, path))
            text = text[pos+len(mk_text):]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        extracted_links = extract_markdown_links(old_node.text)
        if len(extracted_links) == 0:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        for shown, link in extracted_links:
            mk_text = f"[{shown}]({link})"
            pos = text.index(mk_text)
            if pos != 0:
                new_nodes.append(TextNode(text[0:pos], TextType.TEXT))
            new_nodes.append(TextNode(shown, TextType.LINK, link))
            text = text[pos+len(mk_text):]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`" , TextType.CODE)
    return text_nodes

