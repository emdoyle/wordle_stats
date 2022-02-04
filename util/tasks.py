from datetime import datetime
from functools import wraps
from typing import Callable
from zoneinfo import ZoneInfo

from slack_bolt import App

from app.constants import DAILY_TASKS_CUSTOM_KEY, TIMEZONE_CUSTOM_KEY
from app.dataclasses.daily_tasks import DailyTasks
from util.timezone import PACIFIC_TIME


def daily_task(app: "App", attribute_name: str, skip_on_install_day: bool = False):
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
            today = datetime.now(timezone).date()
            if skip_on_install_day and installed_date == today:
                # Do not post on the same day the app was installed
                return
            raw_daily_tasks = installation.get_custom_value(name=DAILY_TASKS_CUSTOM_KEY)
            daily_tasks = (
                DailyTasks.deserialize(data=raw_daily_tasks)
                if raw_daily_tasks is not None
                else DailyTasks()
            )
            if (
                getattr(daily_tasks, attribute_name) is not None
                and getattr(daily_tasks, attribute_name) >= today
            ):
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
