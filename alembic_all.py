import logging
import sys
from typing import List

from admin.databases import database_names, dbpath
from alembic import config


def run_for_databases(arguments: List[str]):
    for database_name in database_names():
        db_path = dbpath(database_name)
        db_driver_url = f"sqlite+pysqlite:///{db_path}"
        print(f"\tRunning for database @ {db_path}")
        try:
            config.main(argv=["-x", f"db_driver_url={db_driver_url}", *arguments])
        except:
            logging.getLogger().exception("Failed to upgrade")
            continue


if __name__ == "__main__":
    run_for_databases(sys.argv[1:])
