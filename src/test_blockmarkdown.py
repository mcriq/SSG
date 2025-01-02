import unittest
from block_markdown import markdown_to_blocks, block_to_block_type


class TestBlockMarkdown(unittest.TestCase):
  def test_markdown_to_blocks(self):
    markdown = """\
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

    block_list = markdown_to_blocks(markdown)
    expected = [
       "# This is a heading",
       "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
       "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
    ]
    self.assertListEqual(block_list, expected)

  def test_markdown_to_blocks_empty_markdown(self):
     markdown = ""
     block_list = markdown_to_blocks(markdown)
     self.assertListEqual(block_list, [])

  def test_block_to_block_type_heading(self):
     md_block = "### Title"
     self.assertEqual(block_to_block_type(md_block), "heading3")
  
  def test_block_to_block_type_code(self):
     md_block = "```This is a code block```"
     self.assertEqual(block_to_block_type(md_block), "code")

  def test_block_to_block_type_quote(self):
      md_block = ">this quote block is a\n>quote is a\n>quote"
      self.assertEqual(block_to_block_type(md_block), "quote")

  def test_block_to_block_type_unordered_list(self):
      md_block = "*List item 1\n*List item 2\n*List item 3"
      self.assertEqual(block_to_block_type(md_block), "unordered list")

  def test_block_to_block_type_ordered_list(self):
      md_block = "1. List item\n2. List item\n3. List item"
      self.assertEqual(block_to_block_type(md_block), "ordered list")
  
  def test_block_to_block_type_paragraph(self):
     md_block = "This is some plain old text"
     self.assertEqual(block_to_block_type(md_block), "paragraph")
  


if __name__ == "__main__":
    unittest.main()