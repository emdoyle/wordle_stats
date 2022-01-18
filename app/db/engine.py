from sqlalchemy import create_engine

from .. import settings

engine = create_engine(f"sqlite+pysqlite:///{settings.DB_PATH}", echo=True, future=True)
