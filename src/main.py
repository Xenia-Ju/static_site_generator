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
            


def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")
    copy_dictree("./static", "./public")

    generate_page("content/index.md", "template.html", "public/index.html")

main()