import unittest
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_olist,
    block_type_ulist,
    block_type_quote,
)


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
  
  def test_block_to_block_types(self):
    block = "# heading"
    self.assertEqual(block_to_block_type(block), block_type_heading)
    block = "```\ncode\n```"
    self.assertEqual(block_to_block_type(block), block_type_code)
    block = "> quote\n> more quote"
    self.assertEqual(block_to_block_type(block), block_type_quote)
    block = "* list\n* items"
    self.assertEqual(block_to_block_type(block), block_type_ulist)
    block = "1. list\n2. items"
    self.assertEqual(block_to_block_type(block), block_type_olist)
    block = "paragraph"
    self.assertEqual(block_to_block_type(block), block_type_paragraph)
  


if __name__ == "__main__":
    unittest.main()