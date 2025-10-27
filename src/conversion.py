import re
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocks import BlockType


#Convert TextNodes to HTMLNodes
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})

    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise ValueError("Invalid TextType")


#Create TextNodes from raw markdown strings
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        elif node.text.count(delimiter) % 2 != 0:
            raise Exception("Missing closing delimiter")

        else:
            sep = node.text.split(delimiter)

            for i in range(len(sep)):
                if i % 2 == 0:
                    if sep[i] != "":
                        new_nodes.append(TextNode(sep[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(sep[i], text_type))

    return new_nodes


#Convert raw markdown to alt and href touples for images and links
def extract_markdown_images(text):
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images


def extract_markdown_links(text):
    images = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return images
#Split raw markdown text into TextNodes based on images and links


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            current_text = node.text
            images = extract_markdown_images(current_text)
            
            for alt_text, url in images:
                parts = current_text.split(f"![{alt_text}]({url})", 1)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                current_text = parts[1]
            
            if current_text:
                new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            current_text = node.text
            links = extract_markdown_links(current_text)
            
            for link_text, url in links:
                parts = current_text.split(f"[{link_text}]({url})", 1)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, url))
                current_text = parts[1]
            
            if current_text:
                new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    input = [TextNode(text, TextType.TEXT)]
    bold = split_nodes_delimiter(input, "**", TextType.BOLD)
    code = split_nodes_delimiter(bold, "`", TextType.CODE)
    image = split_nodes_image(code)
    link = split_nodes_link(image)
    italic = split_nodes_delimiter(link, "_", TextType.ITALIC)
    return italic


def markdown_to_blocks(markdown):
    res = []
    for n in markdown.split("\n\n"):
        n = n.strip()
        if n != '':
            res.append(n)
    return res


def block_to_blocktype(block):
    lines = block.split("\n")
    if block[0:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    elif block[0] == "#" and "#######" not in block:
        for i, char in enumerate(block):
            if char != '#':
                if char == ' ':
                    return BlockType.HEADING
                break
    elif all(line[0] == ">" for line in lines):
        return BlockType.QUOTE
    elif all(line[0:2] == "- " for line in lines):
        return BlockType.UNORDEREDLIST
    elif all(line.split(". ", 1)[0].isdigit() and ". " in line for line in lines):
        if all(int(line.split(". ", 1)[0]) == i + 1 for i, line in enumerate(lines)):
            return BlockType.ORDEREDLIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        blocktype = block_to_blocktype(block)
        if blocktype == BlockType.HEADING:
            level = block.count("#", 0, 6)
            text = block.lstrip("# ").strip()
            textnodes = text_to_textnodes(text)
            htmlnodes = [text_node_to_html_node(node) for node in textnodes]
            children.append(ParentNode(f"h{level}", htmlnodes))
        elif blocktype == BlockType.CODE:
            text = block.strip("```").strip()
            children.append(ParentNode("pre", [ParentNode("code", [LeafNode(None, text)])]))
        elif blocktype == BlockType.QUOTE:
            text = "\n".join(line.lstrip("> ") for line in block.split("\n"))
            textnodes = text_to_textnodes(text)
            htmlnodes = [text_node_to_html_node(node) for node in textnodes]
            children.append(ParentNode("blockquote", htmlnodes))
        elif blocktype in [BlockType.UNORDEREDLIST, BlockType.ORDEREDLIST]:
            tag = "ul" if blocktype == BlockType.UNORDEREDLIST else "ol"
            list_items = []
            for line in block.split("\n"):
                text = line.lstrip("- ").split(". ", 1)[-1]
                textnodes = text_to_textnodes(text)
                htmlnodes = [text_node_to_html_node(node) for node in textnodes]
                list_items.append(ParentNode("li", htmlnodes))
            children.append(ParentNode(tag, list_items))
        else:
            textnodes = text_to_textnodes(block)
            htmlnodes = [text_node_to_html_node(node) for node in textnodes]
            children.append(ParentNode("p", htmlnodes))
    return ParentNode("div", children)

def extract_title(markdown):
    target = "# "
    if target in markdown:
        for line in markdown.split("\n"):
            if line[:2] == target:
               return line.lstrip(target)
    raise Exception("No title")
