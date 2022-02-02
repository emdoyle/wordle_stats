from fastapi import FastAPI, Request
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler

from app import settings
from app.apps import app
from app.listeners import *

api_handler = SlackRequestHandler(app)
api_server = FastAPI()


@api_server.post(settings.SLACK_EVENTS_PATH)
async def events(request: Request):
    return await api_handler.handle(request)


@api_server.get(settings.SLACK_INSTALL_PATH)
async def install(request: Request):
    return await api_handler.handle(request)


@api_server.get(settings.SLACK_OAUTH_REDIRECT_PATH)
async def oauth_redirect(request: Request):
    return await api_handler.handle(request)
