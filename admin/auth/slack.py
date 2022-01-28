import binascii
import os
from typing import Optional
from urllib.parse import urlencode

import aiohttp
from aiohttp import BasicAuth
from fastapi import APIRouter, HTTPException
from fastapi.openapi.models import Response
from fastapi.responses import RedirectResponse

from ..env import env

SLACK_OAUTH_URL = "https://slack.com/oauth/v2/authorize"
SLACK_ACCESS_TOKEN_URL = "https://slack.com/api/oauth.v2.access"
SLACK_CLIENT_ID = env.str("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = env.str("SLACK_CLIENT_SECRET")

SCOPES = [
    "app_mentions:read",
    "channels:history",
    "channels:read",
    "chat:write",
    "groups:read",
    "im:history",
    "im:read",
    "incoming-webhook",
    "mpim:read",
    "users:read",
    "users.profile:read",
    "commands",
]

BASE_URL = env.str("BASE_URL")
OAUTH_REDIRECT_URI = "/oauth-redirect"


STATE = set()


router = APIRouter()


@router.get("/install-to-workspace/")
async def install_to_workspace():
    oauth_url = SLACK_OAUTH_URL
    state_string = str(binascii.hexlify(os.urandom(6)))
    STATE.add(state_string)
    parameters = {
        "scope": ",".join(SCOPES),
        "client_id": SLACK_CLIENT_ID,
        "redirect_uri": f"{BASE_URL}{OAUTH_REDIRECT_URI}",
        "state": state_string,
    }
    oauth_url += f"?{urlencode(parameters)}"
    return RedirectResponse(oauth_url, status_code=302)


@router.get(OAUTH_REDIRECT_URI)
async def handle_oauth_redirect(
    state: str, code: Optional[str] = None, error: Optional[str] = None
):
    if state not in STATE:
        raise HTTPException(
            status_code=400,
            detail="Could not validate oauth request. Please try again.",
        )

    STATE.remove(state)
    if code is None:
        return Response(
            description=f"Wordle was not connected. Reason: {error}", status_code=200
        )
    access_code_payload = {
        "code": code,
        "redirect_uri": f"{BASE_URL}{OAUTH_REDIRECT_URI}",
    }
    async with aiohttp.ClientSession(
        auth=BasicAuth(SLACK_CLIENT_ID, SLACK_CLIENT_SECRET)
    ) as session:
        async with session.post(
            SLACK_ACCESS_TOKEN_URL, data=access_code_payload
        ) as response:
            data = await response.json()
            print(data)
    return Response(description="Wordle was connected successfully!", status_code=200)
