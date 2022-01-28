from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app import settings


def build_engine_for_team_db(team_id: str):
    return create_engine(
        f"sqlite+pysqlite:///{settings.DB_FOLDER}{team_id}{settings.DB_FILE_EXTENSION}",
        echo=True,
        future=True,
    )


engines = {}


def get_engine(team_id: str) -> "Engine":
    if team_id not in engines:
        engines[team_id] = build_engine_for_team_db(team_id=team_id)
    return engines[team_id]
