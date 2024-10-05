from src.textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)

from src.regexmarkdown import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    marked_segment = False
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0 or len(sections) == 1:
            new_nodes.append(old_node)
            continue
        
        for i in range(len(sections)):
            
            if sections[i] == "":
                marked_segment = not marked_segment
                continue
                
            if not marked_segment:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
            
            marked_segment = not marked_segment
                
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    return_nodes = []
    
    for node in old_nodes:
        if not node.text:
            continue

        if not node.text_type == "text":
            return_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        remaining_text = node.text

        for image_alt, image_link in images:
            sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)

            if sections[0]:
                return_nodes.append(TextNode(sections[0], text_type_text))
                remaining_text = remaining_text.replace(sections[0], "", 1)

            return_nodes.append(TextNode(image_alt, text_type_image, image_link))
            remaining_text = remaining_text.replace(f"![{image_alt}]({image_link})", "", 1)

        if remaining_text:
            return_nodes.append(TextNode(remaining_text, text_type_text))

    return return_nodes



def split_nodes_link(old_nodes):
    return_nodes = []
    
    for node in old_nodes:
        if not node.text:
            continue

        if not node.text_type == "text":
            return_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        remaining_text = node.text

        for link_alt, link in links:
            sections = remaining_text.split(f"[{link_alt}]({link})", 1)

            if sections[0]:
                return_nodes.append(TextNode(sections[0], text_type_text))
                remaining_text = remaining_text.replace(sections[0], "", 1)

            return_nodes.append(TextNode(link_alt, text_type_link, link))
            remaining_text = remaining_text.replace(f"[{link_alt}]({link})", "", 1)

        if remaining_text:
            return_nodes.append(TextNode(remaining_text, text_type_text))

    return return_nodes

def text_to_textnodes(text):
    node = TextNode(text, text_type_text)
    nodes = split_nodes_delimiter([node], "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return(nodes)


