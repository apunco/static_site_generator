from enum import Enum
import re

BlockType = Enum("BlockType", ["paragraph", "heading", "code", "quote", "unordered_list", "ordered_list"])

def markdown_to_blocks(markdown):
    split_blocks = re.split(r"\n{2,}", markdown)

    return list(filter(lambda x: x != "", list(map(lambda x: x.strip(), split_blocks))))

def block_to_block_type(block):

    if re.search(r"^\#{1,6} ", block):
        return BlockType.heading
    elif re.search(r"^\`{3}.*?\`{3}$", block, re.DOTALL):
        return BlockType.code
    elif check_quote_block(block):
        return BlockType.quote
    elif check_unordered_list_block(block):
        return BlockType.unordered_list
    elif check_ordered_list_block(block):
        return BlockType.ordered_list
    
    return BlockType.paragraph

def check_quote_block(block):
    if not block:
        return False
    
    split_block = block.split("\n")
    
    for s_block in split_block:
        if not re.search(r"^> ", s_block):
            return False
        
    return True

def check_unordered_list_block(block):
    if not block:
        return False
    
    split_block = block.split("\n")

    for s_block in split_block:
        if not re.search(r"^[\*\-] ",s_block):
            return False
        
    return True

def check_ordered_list_block(block):
    if not block:
        return False
        
    split_block = block.split("\n")

    index = 1

    for s_block in split_block:
        regex = rf"^{index}\. "
        if not re.search(regex,s_block):
            return False
        index += 1
        
    return True

