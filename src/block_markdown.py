import re

def markdown_to_blocks(markdown):
    pattern = r"\n\s*\n"
    block_list = re.split(pattern, markdown)
    block_list_stripped = list(map(lambda block: block.strip(), block_list))
    block_list_space_rem = [block for block in block_list_stripped if block]
    return block_list_space_rem