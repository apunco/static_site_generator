from .htmlNode import *
from .block_markdown import *
from .inline_markdown import *
from .textnode import text_node_to_html_node
from .regexmarkdown import *

def markdown_to_html_node(markdown):
    if markdown is None or markdown == "":
        return HTMLNode("div", [])
    
    block_nodes = markdown_to_blocks(markdown)
    html_nodes = []

    for block in block_nodes:
        html_nodes.append(block_node_to_html_node(block, block_to_block_type(block)))

    return HTMLNode("div", children=html_nodes)

def block_node_to_html_node(block, block_type):

    match block_type:
        case BlockType.quote:
            return HTMLNode("blockquote", children=text_to_children(remove_quote_headings(block)))
        case BlockType.unordered_list:
            return HTMLNode("ul", children=get_list_children(remove_unordered_list_headings(block)))
        case BlockType.ordered_list:
            return HTMLNode("ol", children=get_list_children(remove_ordered_list_headings(block)))            
        case BlockType.code:
            return HTMLNode("pre", children=[HTMLNode("code", remove_code_block_quotes(block))])
        case BlockType.heading:
            return HTMLNode(get_heading_tag(block),None ,children=text_to_children(remove_heading_characters(block)))
        case _:
            return HTMLNode("p", children=text_to_children(block))
    
def get_heading_tag(block):
    level = 0

    while block[level] == "#" and level < 6:
        level += 1

    return f"h{level}"

def get_list_children(block):    
    return list(map(lambda x: HTMLNode("li", text_to_children(x)), block.split("\n")))

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return " ".join(list(map(lambda x: text_node_to_html_node(x).to_html(), text_nodes)))

def extract_title(markdown):
    if markdown is None or markdown == "":
        raise Exception("Missing H1 header")
    
    block_nodes = markdown_to_blocks(markdown)

    for block in block_nodes:
        if block_to_block_type(block) == BlockType.heading and get_heading_tag(block) == "h1":
            return remove_heading_characters(block)
        
    raise Exception("Missing H1 header")         