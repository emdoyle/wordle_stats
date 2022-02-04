from datetime import datetime
from functools import wraps
from typing import Callable
from zoneinfo import ZoneInfo

from slack_bolt import App

from app.constants import DAILY_TASKS_CUSTOM_KEY, TIMEZONE_CUSTOM_KEY
from app.dataclasses.daily_tasks import DailyTasks
from util.timezone import PACIFIC_TIME


def daily_task(
    app: "App",
    attribute_name: str,
    skip_on_install_day: bool = False,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
    microsecond: int = 0,
):
    def decorator(task: Callable):
        @wraps(task)
        def wrapped_task(*, team_id: str, **kwargs):
            installation = app.installation_store.find_installation(
                enterprise_id=None, team_id=team_id
            )
            if installation is None:
                return
            raw_timezone = installation.get_custom_value(name=TIMEZONE_CUSTOM_KEY)
            timezone = (
                ZoneInfo(raw_timezone) if raw_timezone is not None else PACIFIC_TIME
            )
            installed_date = datetime.fromtimestamp(
                installation.installed_at, timezone
            ).date()
            now = datetime.now(timezone)
            threshold_time = now.replace(
                hour=hour, minute=minute, second=second, microsecond=microsecond
            )
            if now < threshold_time:
                # It is not time to process this task yet today
                # (default is threshold_time == beginning of the day)
                return
            today = now.date()
            if skip_on_install_day and installed_date == today:
                # Do not post on the same day the app was installed
                return
            raw_daily_tasks = installation.get_custom_value(name=DAILY_TASKS_CUSTOM_KEY)
            daily_tasks = (
                DailyTasks.deserialize(data=raw_daily_tasks)
                if raw_daily_tasks is not None
                else DailyTasks()
            )
            recorded_date = getattr(daily_tasks, attribute_name)
            if recorded_date is not None and recorded_date >= today:
                # We have already processed this task for this team today.
                return
            task(team_id=team_id, **kwargs)
            setattr(daily_tasks, attribute_name, today)
            installation.set_custom_value(
                name=DAILY_TASKS_CUSTOM_KEY, value=daily_tasks.serialize()
            )
            app.installation_store.save(installation)

        return wrapped_task

    return decorator
