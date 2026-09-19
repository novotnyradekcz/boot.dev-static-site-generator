from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        value: str,
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None or self.value == "":
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None or self.tag == "":
            return self.value
        return f'<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
