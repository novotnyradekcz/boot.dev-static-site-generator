from textnode import TextNode, TextType, extract_markdown_images, extract_markdown_links


class InvalidMarkdownError(Exception):
    pass

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise InvalidMarkdownError("Invalid Markdown syntax; missing delimiter.")
            for i, text in enumerate(split_text):
                if text != "":
                    if i % 2 == 0:
                        new_nodes.append(TextNode(text, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(text, text_type))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                new_nodes.append(node)
            else:
                text = node.text
                for image in images:
                    split_text = text.split(f"![{image[0]}]({image[1]})", 1)
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    text = split_text[1]
                new_nodes.append(TextNode(text, TextType.TEXT))
    return list(filter(lambda node: node.text != "", new_nodes))

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                new_nodes.append(node)
            else:
                text = node.text
                for link in links:
                    split_text = text.split(f"[{link[0]}]({link[1]})", 1)
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    text = split_text[1]
                new_nodes.append(TextNode(text, TextType.TEXT))
    return list(filter(lambda link: link.text != "", new_nodes))
