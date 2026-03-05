from enum import Enum
from htmlnode import *

class TextType(Enum):
    
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "images"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        return True


    def __repr__(self):
        # TextNode(TEXT, TEXT_TYPE, URL)
        return(f"TextNode({self.text}, {self.text_type.value}, {str(self.url)})")

