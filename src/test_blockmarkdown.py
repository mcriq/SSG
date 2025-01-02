import unittest
from block_markdown import markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):
  def test_markdown_to_blocks(self):
    markdown = """
    # This is a heading

    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    * This is the first list item in a list block
    * This is a list item
    * This is another list item
    """

    block_list = markdown_to_blocks(markdown)
    print(block_list)

if __name__ == "__main__":
    unittest.main()