import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestInlineMarkdown(unittest.TestCase):
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

  def test_img_extraction(self):
      text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
      image_list = extract_markdown_images(text)
      self.assertListEqual(
        [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ],
        image_list
      )
  
  def test_link_extraction(self):
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    link_list = extract_markdown_links(text)
    self.assertListEqual(
        [
          ("to boot dev", "https://www.boot.dev"), 
          ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ],
        link_list
    )

  def test_link_extraction_empty_text(self):
      text = ""
      link_list = extract_markdown_links(text)
      self.assertListEqual([], link_list)

  def test_image_extraction_empty_text(self):
      text = ""
      img_list = extract_markdown_images(text)
      self.assertListEqual([], img_list)

if __name__ == "__main__":
    unittest.main()
