def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = [block.strip() for block in markdown.split("\n\n")]
    filtered_blocks = list(filter(lambda block: block != "", blocks))
    return filtered_blocks
