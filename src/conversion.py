import re
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode


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
    tuples = []
    alts = re.findall(r"\[(.*?)\]", text)
    hrefs = re.findall(r"\((https?://.*?)\)", text)
    if len(alts) != len(hrefs):
        raise Exception("Invalid image formatting")
    for i in range(len(alts)):
        tuple = (alts[i], hrefs[i])
        tuples.append(tuple)
    return tuples


#Split raw markdown text into TextNodes based on images and links

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            raise Exception("Nodes can only be TextType.TEXT")
        extract = extract_markdown_images(node.text)
        text_types = list(filter(None, re.split(r"!\[.*?\]\(.*?\)", node.text)))
        ecount = 0
        tcount = 0
        for i in range(len(extract) + len(text_types)):
            if i % 2 == 0:
                new = TextNode(text_types[tcount], TextType.TEXT)
                new_nodes.append(new)
                tcount += 1
            else:
                new = TextNode(extract[ecount][0], TextType.IMAGE, extract[ecount][1])
                new_nodes.append(new)
                ecount += 1
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            raise Exception("Nodes can only be TextType.TEXT")
        extract = extract_markdown_images(node.text)
        text_types = list(filter(None, re.split(r"\[.*?\]\(.*?\)", node.text)))
        ecount = 0
        tcount = 0
        for i in range(len(extract) + len(text_types)):
            if i % 2 == 0:
                new = TextNode(text_types[tcount], TextType.TEXT)
                new_nodes.append(new)
                tcount += 1
            else:
                new = TextNode(extract[ecount][0], TextType.LINK, extract[ecount][1])
                new_nodes.append(new)
                ecount += 1
    return new_nodes
