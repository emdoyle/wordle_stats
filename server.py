from fastapi import FastAPI, Request
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler

from app import settings
from app.apps import app
from app.listeners import *

socket_mode_handler = SocketModeHandler(app, app_token=settings.SLACK_APP_TOKEN)
api_handler = SlackRequestHandler(app)
api_server = FastAPI()


@api_server.on_event("startup")
async def initialize():
    socket_mode_handler.connect()


@api_server.on_event("shutdown")
async def initialize():
    socket_mode_handler.disconnect()


@api_server.get(settings.SLACK_INSTALL_PATH)
async def install(request: Request):
    return await api_handler.handle(request)


@api_server.get(settings.SLACK_OAUTH_REDIRECT_PATH)
async def oauth_redirect(request: Request):
    return await api_handler.handle(request)
