import unittest
from htmlnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_paragraph(self):
      leaf_node = LeafNode("p", "Simple paragraph")
      self.assertEqual(leaf_node.to_html(), "<p>Simple paragraph</p>")

    def test_anchor(self):
      leaf_node = LeafNode("a", "Link Boot", {"href": "https://www.boot.dev", "target": "_blank"})
      self.assertEqual(leaf_node.to_html(), '<a href="https://www.boot.dev" target="_blank">Link Boot</a>')

    def test_no_tag(self):
      leaf_node = LeafNode(None, "raw text")
      self.assertEqual(leaf_node.to_html(), "raw text")

    def test_no_value(self):
      with self.assertRaises(ValueError):
         leaf_node = LeafNode("p", None)
         leaf_node.to_html()

if __name__ == "__main__":
    unittest.main()
