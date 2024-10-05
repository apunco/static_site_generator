import shutil
import os
from generate_page import generate_pages_recursive

def main():

    shutil.rmtree("./public/", ignore_errors=True)
    copy_static_files("./static", "./public")

    generate_pages_recursive("./content", "./template.html", "./public")

def copy_static_files(source_path, target_path):
    if not os.path.exists(target_path):
        os.mkdir(target_path)

    tree = os.listdir(source_path)

    for item in tree:
        temp_path = os.path.join(source_path, item)

        if os.path.isdir(temp_path):
            copy_static_files(temp_path, os.path.join(target_path, item))
        else:
            shutil.copy(temp_path, os.path.join(target_path, item))


main()
