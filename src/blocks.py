from enum import Enum


class BlockType(Enum):
    HEADING = "### Heading"
    CODE = "```Code```"
    QUOTE = ">Quote"
    UNORDEREDLIST = "- Unordered List"
    ORDEREDLIST = "1. Ordered List"
    PARAGRAPH = "Default Paragraph"
