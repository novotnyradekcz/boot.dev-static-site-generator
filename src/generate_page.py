import os

from block import markdown_to_html_node


def extract_title(markdown: str):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("Missing title - no h1 (#) header present in markdown.")

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'...")

    with open(from_path, 'r') as file:
        markdown = file.read()
    with open(template_path, 'r') as file:
        template = file.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    with open(dest_path, 'w') as file:
        print(f"Wrote {file.write(html)} characters of HTML to '{dest_path}'.")
