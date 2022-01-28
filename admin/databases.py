from os import listdir
from os.path import isfile
from typing import List

from app import settings


def dbpath(filename: str) -> str:
    return f"{settings.DB_FOLDER}{filename}"


def database_names() -> List[str]:
    return [
        filename
        for filename in filter(
            lambda _file: isfile(dbpath(_file))
            and _file.endswith(settings.DB_FILE_EXTENSION),
            listdir(settings.DB_FOLDER),
        )
    ]
