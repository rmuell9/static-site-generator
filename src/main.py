from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode


def main():
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    print(parent_node.to_html())

main()
