from textnode import *
from htmlnode import *
import re
from enum import Enum


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
            return LeafNode("a", textnode.text, props = {"href": textnode.url})
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


def markdown_to_blocks(markdown):
    blocks = []
    current = []
    for line in markdown.split("\n"):
        line = line.strip()
        if not line:
            if current:
                blocks.append("\n".join(current))
                current = []
            continue
        current.append(line)
    if current:
        blocks.append("\n".join(current))
    return blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def block_to_block_type(block):
    if not block:
        return BlockType.PARAGRAPH
    if re.findall(r"^#{1,6} ", block):
        return BlockType.HEADING
    if re.findall(r"^```", block) and re.findall(r"```$", block):
        return BlockType.CODE
    if block[0] == ">":
        return BlockType.QUOTE
    if len(re.findall(r"^- ", block, re.M)) == len(block.split("\n")):
        return BlockType.UNORDERED
    if len(re.findall(r"^\d+. ", block, re.M)) == len(block.split("\n")):
        check = re.findall(r"^\d+", block, re.M)
        for i, j in enumerate(check, 1):
            if str(i) != j:
                print("here?")
                return BlockType.PARAGRAPH
        return BlockType.ORDERED
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            childnodes_t = text_to_textnodes(block)
            childnodes = []
            for child in childnodes_t:
                childnodes.append(text_node_to_html_node(child))
            node = ParentNode("p", childnodes)
            html_nodes.append(node)
        if block_type == BlockType.HEADING:
            level = len(re.findall(r"^#{1,6} ", block)[0])
            tag = "h" + str(level-1)
            childnodes_t = text_to_textnodes(block[level:])
            childnodes = []
            for child in childnodes_t:
                childnodes.append(text_node_to_html_node(child))
            node = ParentNode(tag, childnodes)
            html_nodes.append(node)
        if block_type == BlockType.CODE:
            childnode = LeafNode("code", block[3:-3])
            node = ParentNode("pre", [childnode])
            html_nodes.append(node)
        if block_type == BlockType.UNORDERED:
            linenodes = []
            for line in block.split("\n"):
                childnodes_t = text_to_textnodes(line[2:])
                childnodes = []
                for child in childnodes_t:
                    childnodes.append(text_node_to_html_node(child))
                linenodes.append(ParentNode("li", childnodes))
            node = ParentNode("ul", linenodes)
            html_nodes.append(node)
        if block_type == BlockType.ORDERED:
            linenodes = []
            for line in block.split("\n"):
                exclusion = len(re.findall(r"^\d+. ", line)[0])
                childnodes_t = text_to_textnodes(line[exclusion:])
                childnodes = []
                for child in childnodes_t:
                    childnodes.append(text_node_to_html_node(child))
                linenodes.append(ParentNode("li", childnodes))
            node = ParentNode("ol", linenodes)
            html_nodes.append(node)
        if block_type == BlockType.QUOTE:
            childnodes_t = text_to_textnodes(block[1:].strip())
            childnodes = []
            for child in childnodes_t:
                childnodes.append(text_node_to_html_node(child))
            node = ParentNode("blockquote", childnodes)
            html_nodes.append(node)
    return ParentNode("div", html_nodes)
 


