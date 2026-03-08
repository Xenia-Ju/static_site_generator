from textnode import *
from htmlnode import *
from generate_html import *
import os
import shutil


def copy_dictree(source, target):
    content = os.listdir(source)
    for file in content:
        path = os.path.join(source, file)
        if os.path.isfile(path):
            shutil.copy2(path, os.path.join(target, file))
        else:
            os.mkdir(os.path.join(target, file))
            copy_dictree(path, os.path.join(target, file))
            
def generate_pages_recursive(dir_content, template, dir_destination):
    content_content = os.listdir(dir_content)
    content_destination = os.listdir(dir_destination)
    for file in content_content:
        if file in content_destination:
            continue
        path = os.path.join(dir_content, file)
        if not os.path.isfile(path):
            os.mkdir(os.path.join(dir_destination, file))
            generate_pages_recursive(path, template, os.path.join(dir_destination, file))
            continue
        if file.endswith(".md"):
            generate_page(path, template, os.path.join(dir_destination, file[:-3]+".html"))
        
def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")
    copy_dictree("./static", "./public")

    generate_pages_recursive("./content", "template.html", "./public")
    #generate_page("./content/index.md", template, "./public/index.html"))
    
main()