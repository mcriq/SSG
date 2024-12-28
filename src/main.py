from textnode import TextNode, TextType
# hello world
def main():
  new_node = TextNode("This is a textnode", TextType.BOLD, "https://www.boot.dev")
  print(new_node)

main()