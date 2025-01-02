import re

def markdown_to_blocks(markdown):
    pattern = r"\n\s*\n"
    block_list = re.split(pattern, markdown)
    block_list_stripped = list(map(lambda block: block.strip(), block_list))
    block_list_space_rem = [block for block in block_list_stripped if block]
    return block_list_space_rem

def block_to_block_type(md_block):
    if md_block[0] == "#":
        count = 0
        for char in md_block:
            if char != "#":
                break
            if count < 6:
                count += 1
        return f"heading{count}"

    if md_block[:3] == "```" and md_block[-3:] == "```":
        return "code"

    if md_block[0] == ">":
        is_quote = True
        for block in md_block.split("\n"):
            if block.startswith(">"):
                continue
            else:
                is_quote = False
                break
        if is_quote:
            return "quote"
    
    if md_block[0] == "*" or md_block[0] == "-":
        is_unordered_list = True
        for block in md_block.split("\n"):
            if block.startswith("*") or block.startswith("-"):
                continue
            else:
                is_unordered_list = False
                break
        if is_unordered_list:
            return "unordered list"
    
    if md_block[:3] == "1. ":
        is_ordered_list = True
        curr_digit = 0
        for block in md_block.split("\n"):
            curr_digit += 1
            if block[0].isdigit() and block[:3] == f"{curr_digit}. ":
                continue
            else:
                is_ordered_list = False
                break
        if is_ordered_list:
            return "ordered list"

    else:
        return "paragraph"