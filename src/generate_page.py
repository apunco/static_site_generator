from markdown import markdown_to_html_node, extract_title
import os

def generate_pages_recursive(from_path, template_path, dest_path):
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    for item in os.listdir(from_path):
        temp_path = os.path.join(dest_path, item)
        temp_from_path = os.path.join(from_path, item)

        if os.path.isdir(temp_from_path):
            generate_pages_recursive(temp_from_path, template_path, temp_path)
        else:
            print(f"Generating page from {temp_from_path} to {temp_path} using {template_path}")
            markdown_file = open(temp_from_path, "r")
            markdown = markdown_file.read()

            template_file = open(template_path, "r")
            template = template_file.read()

            html_string = markdown_to_html_node(markdown).to_html()
            page_title = extract_title(markdown)

            page_string = template.replace("{{ Title }}", page_title).replace("{{ Content }}", html_string)

            html_output_file = open(os.path.join(dest_path, "index.html"), "x")
            html_output_file.write(page_string)
            html_output_file.close()


    