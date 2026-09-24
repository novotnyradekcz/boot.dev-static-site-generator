from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None or self.tag == "":
            raise ValueError("ParentNode must have a tag.")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have children.")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
