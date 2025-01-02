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

def split_nodes_image(old_nodes):
  new_nodes = []
  for old_node in old_nodes:
    if old_node.text_type != TextType.TEXT:
      new_nodes.append(old_node)
      continue
    original_text = old_node.text
    images = extract_markdown_images(original_text)
    if len(images) == 0:
      new_nodes.append(old_node)
      continue
    for image in images:
      sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
      if len(sections) != 2:
        raise ValueError("Invalid markdown, image section not closed")
      if sections[0] != "":
        new_nodes.append(TextNode(sections[0], TextType.TEXT))
      new_nodes.append(
        TextNode(
                  image[0],
                  TextType.IMAGE,
                  image[1],
                )
      )
      original_text = sections[1]
    if original_text != "":
      new_nodes.append(TextNode(original_text, TextType.TEXT))
  return new_nodes


def split_nodes_link(old_nodes):
  new_nodes = []
  for old_node in old_nodes:
    if old_node.text_type != TextType.TEXT:
      new_nodes.append(old_node)
      continue
    original_text = old_node.text
    links = extract_markdown_links(original_text)
    if len(links) == 0:
      new_nodes.append(old_node)
      continue
    for link in links:
      sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
      if len(sections) != 2:
        raise ValueError("Invalid markdown, link section not closed")
      if sections[0] != "":
        new_nodes.append(TextNode(sections[0], TextType.TEXT))
      new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
      original_text = sections[1]
    if original_text != "":
      new_nodes.append(TextNode(original_text, TextType.TEXT))
  return new_nodes

def text_to_textnodes(text):
  if text == "":
    return []
  nodes = [TextNode(text, TextType.TEXT)]
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
  nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
  nodes = split_nodes_image(nodes)
  nodes = split_nodes_link(nodes)
  return nodes