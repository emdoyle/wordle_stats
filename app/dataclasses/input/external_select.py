from dataclasses import dataclass
from typing import Optional, Union

from ..section import MrkdwnBlock, PlainTextBlock


@dataclass
class SelectOption:
    text: PlainTextBlock
    value: str


@dataclass
class ExternalSelect:
    action_id: str
    placeholder: PlainTextBlock
    initial_option: Optional[SelectOption] = None
    min_query_length: int = 3
    type: str = "external_select"


@dataclass
class ExternalSelectSection:
    text: Union[PlainTextBlock, MrkdwnBlock]
    accessory: ExternalSelect
    type: str = "section"
