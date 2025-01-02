import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


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

  def test_split_image(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ],
        new_nodes,
    )

  def test_split_image_single(self):
    node = TextNode(
        "![image](https://www.example.COM/IMAGE.PNG)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
        ],
        new_nodes,
    )

  def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ],
        new_nodes,
    )

  def test_split_links(self):
    node = TextNode(
        "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
          TextNode("This is text with a ", TextType.TEXT),
          TextNode("link", TextType.LINK, "https://boot.dev"),
          TextNode(" and ", TextType.TEXT),
          TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
          TextNode(" with text that follows", TextType.TEXT),
        ],
        new_nodes,
    )

  def test_text_to_textnodes_all_types(self):
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    nodes = text_to_textnodes(text)
    output = [
      TextNode("This is ", TextType.TEXT),
      TextNode("text", TextType.BOLD),
      TextNode(" with an ", TextType.TEXT),
      TextNode("italic", TextType.ITALIC),
      TextNode(" word and a ", TextType.TEXT),
      TextNode("code block", TextType.CODE),
      TextNode(" and an ", TextType.TEXT),
      TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
      TextNode(" and a ", TextType.TEXT),
      TextNode("link", TextType.LINK, "https://boot.dev"),
    ]
    self.assertListEqual(nodes, output)

  def test_text_to_textnodes_blank(self):
    text = ""
    nodes = text_to_textnodes(text)
    self.assertListEqual(nodes, [])

  def test_text_to_textnodes_nested(self):
     text = "This is **bold text with *italics* inside of it**"
     nodes = text_to_textnodes(text)
     output = [
      TextNode("This is ", TextType.TEXT),
      TextNode("bold text with *italics* inside of it", TextType.BOLD)
     ]
     self.assertListEqual(nodes, output)

  def test_text_to_textnodes_malformed(self):
    with self.assertRaises(Exception):
      text = "This **bold text is malformed"
      text_to_textnodes(text)
if __name__ == "__main__":
    unittest.main()
