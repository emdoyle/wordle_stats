from fastapi import FastAPI, Request
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.starlette.handler import to_bolt_request
from starlette.responses import JSONResponse

from app import settings
from app.apps import app
from app.blocks.timezone import get_timezone_options
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


@api_server.post(settings.TIMEZONE_OPTIONS_PATH)
async def handle_timezone_options(request: Request):
    body = await request.body()
    request = to_bolt_request(request, body)
    print(request.body)
    return JSONResponse(content=get_timezone_options())
