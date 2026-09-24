import re
from enum import Enum

from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextType, TextNode, text_node_to_html_node, text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unoreder_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = [block.strip() for block in markdown.split("\n\n")]
    filtered_blocks = list(filter(lambda block: block != "", blocks))
    return filtered_blocks

def is_valid_ordered_list(lines: list[str]) -> bool:
    for expected_num, line in enumerate(lines, start=1):
        match = re.match(r"^(\d+)\.\s+", line)
        if not match:
            return False
        if int(match.group(1)) != expected_num:
            return False
    return True

def block_to_block_type(block: str) -> BlockType:
    lines = block.splitlines()
    if not lines:
        return BlockType.PARAGRAPH

    if len(lines) == 1 and re.match(r"^#{1,6}\s+.+", lines[0]):
        return BlockType.HEADING

    if len(lines) >= 2 and lines[0].strip() == "```" and lines[-1].strip() == "```":
        return BlockType.CODE

    if all(re.match(r"^> ?", line) for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if is_valid_ordered_list(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block: str) -> ParentNode:
    level = len(block.split(" ", 1)[0])
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    children = text_to_children(block[level + 1:])
    return ParentNode(f"h{level}", children)

def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    raw_text_node = TextNode(block[4:-3], TextType.TEXT)
    code = ParentNode("code", [text_node_to_html_node(raw_text_node)])
    return ParentNode("pre", [code])

def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines: list[str] = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    return ParentNode("blockquote", text_to_children(" ".join(new_lines)))

def ulist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items: list[HTMLNode] = []
    for item in items:
        children = text_to_children(item[2:])
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def olist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items: list[HTMLNode] = []
    for item in items:
        html_items.append(ParentNode("li", text_to_children(item.split(". ", 1)[1])))
    return ParentNode("ol", html_items)

def block_to_node(block: str) -> HTMLNode:
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return ulist_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return olist_to_html_node(block)

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    nodes: list[HTMLNode] = []
    for block in blocks:
        nodes.append(block_to_node(block))
    return ParentNode("div", nodes, None)
