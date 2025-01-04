import os
import shutil
from textnode import TextNode, TextType

def copy_content(source_path, dest_path):
  if not os.path.exists(source_path):
    raise Exception("Cannot copy from non-existent directory")
  if os.path.exists(dest_path):
    print(f'Deleting {dest_path} folder and contents...')
    shutil.rmtree(dest_path)
  os.mkdir(dest_path)
  source_dir = os.listdir(source_path)
  for item in source_dir:
    source_full_path = os.path.join(source_path, item)
    dest_full_path = os.path.join(dest_path, item)
    if os.path.isfile(source_full_path):
      shutil.copy(source_full_path, dest_full_path)
      print(f"Copying file {source_full_path} to {dest_full_path}")
    else:
      os.mkdir(dest_full_path)
      copy_content(source_full_path, dest_full_path)




def main():
  copy_content("static", "public")

main()
  # new_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
  # print(new_node)