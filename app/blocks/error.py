from dataclasses import asdict
from typing import Dict

from ..dataclasses import PlainTextBlock, PlainTextSection


def get_error_block(error: Exception) -> Dict:
    return asdict(
        PlainTextSection(
            text=PlainTextBlock(
                text=f"Error: {error}",
                emoji=True,
            )
        )
    )
