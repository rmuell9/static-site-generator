from textnode import TextType
from textnode import TextNode


def main():
    dummy = TextNode("hello", TextType.LINK, "google.com")
    print(dummy)


main()
