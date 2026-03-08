from converter import *
import htmlnode
import textnode
import os


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line[0:2] == "# ":
            return line[2:].strip()
    raise Exception


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file = open(from_path)
    markdown = file.read()
    file.close()
    file = open(template_path)
    template = file.read()
    file.close()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    template = template.replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")
    file = open(dest_path, "w")
    file.write(template)
    file.close()