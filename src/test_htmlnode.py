import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
  def test_to_html_props(self):
    node = HTMLNode(
        "div",
        "Hello, world!",
        None,
        {"class": "greeting", "href": "https://boot.dev"},
    )
    self.assertEqual(
        node.props_to_html(),
        ' class="greeting" href="https://boot.dev"',
    )

  def test_values(self):
    node = HTMLNode(
        "div",
        "I wish I could read",
    )
    self.assertEqual(
        node.tag,
        "div",
    )
    self.assertEqual(
        node.value,
        "I wish I could read",
    )
    self.assertEqual(
        node.children,
        None,
    )
    self.assertEqual(
        node.props,
        None,
    )

  def test_repr(self):
    node = HTMLNode(
        "p",
        "What a strange world",
        None,
        {"class": "primary"},
    )
    self.assertEqual(
        node.__repr__(),
        "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
    )

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
