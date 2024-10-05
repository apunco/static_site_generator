import re

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches
    
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text) 
    return matches

def remove_quote_headings(block):
    return re.sub(r"^> ", "", block, flags=re.MULTILINE)

def remove_unordered_list_headings(block):
    return re.sub(r"^\* ", "", block, flags=re.MULTILINE)

def remove_ordered_list_headings(block):
    return re.sub(r"^\d. ", "", block, flags=re.MULTILINE)

def remove_code_block_quotes(block):
    return re.sub(r"^```[\w]*\n|```$", "", block, flags=re.MULTILINE)

def remove_heading_characters(block):
    return re.sub(r"^#{1,6} ", "", block).strip()




    
