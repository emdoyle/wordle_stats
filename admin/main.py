# responsibilities
# - OAuth flow with Slack
#   - web server (FastAPI?)
# - manage bot servers (and data)
#   - docker_py
#     - spin_up == create volume, build server image, run server container with volume, secrets, crontab config mounted
#     - tear_down == stop and remove container, remove volumes
#     - upgrade == (look into docker service) stop container, rebuild image (try to frontload), start container
#       - also may need to use an entrypoint file to run migrations before server starts
from fastapi import FastAPI

from .auth.slack import router as auth_router

app = FastAPI()

app.include_router(router=auth_router)
