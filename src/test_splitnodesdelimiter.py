import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter


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
    self.assertListEqual(
      [
        TextNode("Text with ", TextType.TEXT),
        TextNode("multiple", TextType.CODE),
        TextNode(" different ", TextType.TEXT),
        TextNode("code blocks", TextType.CODE),
      ],
      nodes
    )

  def test_split_nodes_not_text_type(self):
    node = TextNode("This is a code block", TextType.CODE)
    nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertListEqual(
      [
        TextNode("This is a code block", TextType.CODE),
      ],
      nodes
    )

  def test_split_nodes_empty_string(self):
    node = TextNode("", TextType.TEXT)
    nodes = split_nodes_delimiter([node], "`", TextType.TEXT)
    self.assertListEqual(
      [
        TextNode("", TextType.TEXT)
      ],
      nodes
    )
  
  def test_delim_bold_and_italic(self):
    node = TextNode("**bold** and *italic*", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
    self.assertListEqual(
        [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ],
        new_nodes,
    )

  def test_split_nodes_unmatched_delim(self):
    with self.assertRaises(Exception):
      node = TextNode("String with *bad markdown.", TextType.TEXT)
      split_nodes_delimiter([node], "*", TextType.ITALIC)

if __name__ == "__main__":
    unittest.main()
