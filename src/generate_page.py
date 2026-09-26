import os

from block import markdown_to_html_node


def extract_title(markdown: str):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("Missing title - no h1 (#) header present in markdown.")

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'...")

    with open(from_path, 'r') as file:
        markdown = file.read()
    with open(template_path, 'r') as file:
        template = file.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = (
        template
            .replace("{{ Title }}", title)
            .replace("{{ Content }}", content)
            .replace('href="/', f'href="{basepath}')
            .replace('src="/', f'src="{basepath}')
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        print(f"Wrote {file.write(html)} characters of HTML to '{dest_path}'.")

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str):
    src = os.path.abspath(dir_path_content)
    dst = os.path.abspath(dest_dir_path)
    contents = os.listdir(src)
    for content in contents:
        if os.path.isfile(os.path.join(src, content)) and content.endswith(".md"):
            generate_page(os.path.join(src, content), template_path, os.path.join(dst, content[:-2] + "html"), basepath)
        else:
            generate_pages_recursive(os.path.join(src, content), template_path, os.path.join(dst, content), basepath)
