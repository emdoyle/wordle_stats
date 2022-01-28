from typing import List

from admin.databases import database_names
from app import settings


# TODO: pull from installations data dir
def installed_team_ids() -> List[str]:
    return [db_name[: -len(settings.DB_FILE_EXTENSION)] for db_name in database_names()]
