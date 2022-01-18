from dataclasses import dataclass
from typing import Optional


@dataclass
class PlainTextInput:
    action_id: Optional[str] = None
    multiline: Optional[bool] = False
    type: str = "plain_text_input"


@dataclass
class PlainTextLabel:
    text: str
    emoji: Optional[bool] = False
    type: str = "plain_text"


@dataclass
class MultiLineTextInputBlock:
    element: PlainTextInput
    label: PlainTextLabel
    dispatch_action: bool = True
    type: str = "input"
