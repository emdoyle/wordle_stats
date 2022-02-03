from dataclasses import dataclass
from datetime import date, datetime
from typing import Dict, Optional

from app.constants import ISO_DATE_FORMAT


@dataclass
class DailyTasks:
    solution_thread_posted: Optional[date] = None
    shoutout_winners_posted: Optional[date] = None

    def serialize(self) -> Dict:
        solution_thread_posted = self.solution_thread_posted
        if solution_thread_posted is not None:
            solution_thread_posted = solution_thread_posted.strftime(ISO_DATE_FORMAT)
        shoutout_winners_posted = self.shoutout_winners_posted
        if shoutout_winners_posted is not None:
            shoutout_winners_posted = shoutout_winners_posted.strftime(ISO_DATE_FORMAT)
        return {
            "solution_thread_posted": solution_thread_posted,
            "shoutout_winners_posted": shoutout_winners_posted,
        }

    @classmethod
    def deserialize(cls, data: Dict) -> "DailyTasks":
        solution_thread_posted = data.get("solution_thread_posted")
        if solution_thread_posted is not None:
            solution_thread_posted = datetime.strptime(
                solution_thread_posted, ISO_DATE_FORMAT
            ).date()
        shoutout_winners_posted = data.get("shoutout_winners_posted")
        if shoutout_winners_posted is not None:
            shoutout_winners_posted = datetime.strptime(
                shoutout_winners_posted, ISO_DATE_FORMAT
            ).date()
        return cls(
            solution_thread_posted=solution_thread_posted,
            shoutout_winners_posted=shoutout_winners_posted,
        )
