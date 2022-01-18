from dataclasses import dataclass
from typing import Optional


@dataclass
class PlainTextBlock:
    text: str
    emoji: Optional[bool] = False
    type: str = "plain_text"


@dataclass
class PlainTextSection:
    text: PlainTextBlock
    type: str = "section"
