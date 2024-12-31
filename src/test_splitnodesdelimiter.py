import unittest
from textnode import TextNode, TextType
from splitnodesdelimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
  def test_split_nodes_no_delim(self):
    node = TextNode("Just plain text", TextType.TEXT)
    nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(len(nodes), 1)
    self.assertEqual(nodes[0].text, 'Just plain text')
    self.assertEqual(nodes[0].text_type, TextType.TEXT)

  def test_split_nodes_multi_delim(self):
    node = TextNode("Text with `multiple` different `code blocks`", TextType.TEXT)
    nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(len(nodes), 4)
    self.assertEqual(nodes[0].text, "Text with ")
    self.assertEqual(nodes[0].text_type, TextType.TEXT)
    self.assertEqual(nodes[1].text, "multiple")
    self.assertEqual(nodes[1].text_type, TextType.CODE)
    self.assertEqual(nodes[2].text, " different ")
    self.assertEqual(nodes[2].text_type, TextType.TEXT)
    self.assertEqual(nodes[3].text,  "code blocks")
    self.assertEqual(nodes[3].text_type, TextType.CODE)

  def test_split_nodes_not_text_type(self):
    node = TextNode("This is a code block", TextType.CODE)
    nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(len(nodes), 1)
    self.assertEqual(nodes[0].text, "This is a code block")
    self.assertEqual(nodes[0].text_type, TextType.CODE)

  def test_split_nodes_empty_string(self):
    node = TextNode("", TextType.TEXT)
    nodes = split_nodes_delimiter([node], "`", TextType.TEXT)
    self.assertEqual(len(nodes), 1)
    self.assertEqual(nodes[0].text, "")
    self.assertEqual(nodes[0].text_type, TextType.TEXT)

  def test_split_nodes_unmatched_delim(self):
    with self.assertRaises(Exception):
      node = TextNode("String with *bad markdown.", TextType.TEXT)
      split_nodes_delimiter([node], "*", TextType.ITALIC)

if __name__ == "__main__":
    unittest.main()
