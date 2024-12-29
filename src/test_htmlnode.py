import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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

  def test_parent_no_tag(self):
    with self.assertRaises(ValueError):
      parent_node = ParentNode(None, [LeafNode("p", "Small paragraph")])
      parent_node.to_html()
  
  def test_single_child(self):
    parent_node = ParentNode("div", [LeafNode("p", "Small paragraph")])
    self.assertEqual(parent_node.to_html(), "<div><p>Small paragraph</p></div>")

  def test_no_child(self):
    with self.assertRaises(ValueError):
      parent_node = ParentNode("div", None, None)
      parent_node.to_html()
  
  def test_multi_child(self):
    parent_node = ParentNode("div", [LeafNode("p", "Small paragraph"), LeafNode("p", "Another paragraph")])
    self.assertEqual(parent_node.to_html(), "<div><p>Small paragraph</p><p>Another paragraph</p></div>")
  
  def test_nested_parent(self):
    parent_node = ParentNode("div", [ParentNode("span", [LeafNode("p", "Small paragraph")]), LeafNode("a", "Link", {"href": "https://www.boot.dev"})])
    self.assertEqual(parent_node.to_html(), '<div><span><p>Small paragraph</p></span><a href="https://www.boot.dev">Link</a></div>')

  def test_parent_props(self):
    parent_node = ParentNode("div", [LeafNode("p", "Small paragraph")], {"class": "main"})
    self.assertEqual(parent_node.to_html(), '<div class="main"><p>Small paragraph</p></div>')

if __name__ == "__main__":
    unittest.main()
