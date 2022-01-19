from dataclasses import dataclass, field
from enum import IntEnum
from typing import Dict, List, Optional, Tuple

from app.constants import WORDLE_MAX_ATTEMPTS, WORDLE_WORD_LENGTH


class BlockColor(IntEnum):
    BLACK = 1
    YELLOW = 2
    GREEN = 3


BLOCK_COLOR_BY_EMOJI = {
    "⬛": BlockColor.BLACK,
    "🟨": BlockColor.YELLOW,
    "🟩": BlockColor.GREEN,
}  # type: Dict[str, "BlockColor"]


@dataclass
class WordleLine:
    blocks: Tuple[BlockColor, BlockColor, BlockColor, BlockColor, BlockColor] = field(
        default_factory=lambda: (
            BlockColor.BLACK,
            BlockColor.BLACK,
            BlockColor.BLACK,
            BlockColor.BLACK,
            BlockColor.BLACK,
        )
    )

    @classmethod
    def parse(cls, raw_line: str) -> "WordleLine":
        line = raw_line.strip()
        if len(line) != WORDLE_WORD_LENGTH:
            raise ValueError(
                f"Could not parse Wordle score. Malformed line received: {raw_line}"
            )

        blocks = (
            BLOCK_COLOR_BY_EMOJI[line[0]],
            BLOCK_COLOR_BY_EMOJI[line[1]],
            BLOCK_COLOR_BY_EMOJI[line[2]],
            BLOCK_COLOR_BY_EMOJI[line[3]],
            BLOCK_COLOR_BY_EMOJI[line[4]],
        )
        return cls(blocks=blocks)

    @property
    def is_winning_line(self) -> bool:
        return all((block == BlockColor.GREEN for block in self.blocks))


@dataclass
class WordleScore:
    edition: int
    attempts: Optional[int] = None
    lines: List[WordleLine] = field(default_factory=list)

    @classmethod
    def parse(cls, raw_score: str) -> "WordleScore":
        """
        example:

        Wordle 213 5/6

        ⬛⬛⬛⬛⬛
        ⬛⬛🟨⬛🟨
        ⬛🟩🟩⬛⬛
        ⬛🟩🟩⬛⬛
        🟩🟩🟩🟩🟩

        """
        wordle_score = cls(edition=0, attempts=None)

        raw_lines = iter(raw_score.split("\n"))
        top_line = next(
            (line for line in raw_lines if line.strip().startswith("Wordle")), None
        )
        if top_line is None:
            raise ValueError(
                "Could not parse Wordle score. 'Wordle <edition> <score>' line not found."
            )
        try:
            _, edition, attempts = top_line.split(" ")
            wordle_score.edition = int(edition)
            wordle_score.attempts = int(attempts[0])
        except (ValueError, IndexError):
            raise ValueError("Could not parse Wordle score. Top score line malformed.")

        score_lines = wordle_score.attempts
        for line in raw_lines:
            if not line.strip():
                # Skip any number of blank lines
                continue

            wordle_line = WordleLine.parse(line)
            wordle_score.lines.append(wordle_line)

            score_lines -= 1
            if not score_lines:
                # If we have a score line for each attempt, ignore the rest
                break

        return wordle_score

    def validate(self, raise_error: bool = False) -> bool:
        if self.attempts != len(self.lines) or self.attempts > WORDLE_MAX_ATTEMPTS:
            if raise_error:
                raise ValueError(
                    f"Wordle score invalid. Number of attempts {self.attempts} does not match "
                    f"number of lines ({len(self.lines)}) "
                    f"or is above {WORDLE_MAX_ATTEMPTS}."
                )
            return False
        final_attempt_index = self.attempts - 1
        return self.lines[final_attempt_index].is_winning_line