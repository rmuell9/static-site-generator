import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "BIG TITLE")
        node2 = HTMLNode("h1", "BIG TITLE")
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
