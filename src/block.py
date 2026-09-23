import re
from enum import Enum


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
