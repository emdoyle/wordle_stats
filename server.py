import logging
import sys
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, Request
from slack_bolt.adapter.fastapi import SlackRequestHandler

from app import settings
from app.apps import app
from app.listeners import *

api_handler = SlackRequestHandler(app)
api_server = FastAPI()


logging.basicConfig(
    level=settings.LOG_LEVEL,
    handlers=[
        logging.StreamHandler(sys.stdout),
        RotatingFileHandler(
            filename=settings.LOG_FILE_NAME, maxBytes=settings.MAX_LOG_FILE_BYTES
        ),
    ],
)


@api_server.post(settings.SLACK_EVENTS_PATH)
async def events(request: Request):
    return await api_handler.handle(request)


@api_server.get(settings.SLACK_INSTALL_PATH)
async def install(request: Request):
    return await api_handler.handle(request)


@api_server.get(settings.SLACK_OAUTH_REDIRECT_PATH)
async def oauth_redirect(request: Request):
    return await api_handler.handle(request)
