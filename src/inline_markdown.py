import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes_list = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT or delimiter not in node.text:
      new_nodes_list.append(node)
      continue
    
    if node.text.count(delimiter) % 2 != 0:
        raise Exception("Unmatched delimiter found")
    
    text_list = node.text.split(delimiter)
    delimited_node_list = []

    for i in range(0, len(text_list)):
      if text_list[i] == "":
        continue
      elif i % 2 == 0:
        delimited_node_list.append(TextNode(text_list[i], TextType.TEXT))
      else:
        delimited_node_list.append(TextNode(text_list[i], text_type))
    new_nodes_list.extend(delimited_node_list)
  return new_nodes_list

def extract_markdown_images(text):
  pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  return matches
  
def extract_markdown_links(text):
  pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  return matches