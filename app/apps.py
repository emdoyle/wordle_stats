import logging
from logging.handlers import RotatingFileHandler

from slack_bolt import App, BoltResponse
from slack_bolt.oauth.callback_options import CallbackOptions, FailureArgs, SuccessArgs
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

from util.timezone import PACIFIC_TIMEZONE_NAME

from . import settings
from .constants import TIMEZONE_CUSTOM_KEY
from .db import Base, get_engine

logging.basicConfig(
    level=settings.LOG_LEVEL,
    handlers=[
        RotatingFileHandler(
            filename=settings.LOG_FILE_NAME, maxBytes=settings.MAX_LOG_FILE_BYTES
        ),
    ],
)

SCOPES = [
    "app_mentions:read",
    "channels:read",
    "chat:write",
    "groups:read",
    "im:history",
    "im:read",
    "mpim:read",
    "users:read",
    "users.profile:read",
    "commands",
]


# TODO: do all this asynchronously
def oauth_success(args: SuccessArgs) -> BoltResponse:
    installation = args.installation
    installation.set_custom_value(name=TIMEZONE_CUSTOM_KEY, value=PACIFIC_TIMEZONE_NAME)
    args.settings.installation_store.save(installation)
    Base.metadata.create_all(get_engine(team_id=installation.team_id))
    return BoltResponse(
        status=302,
        headers={
            "Location": f"{settings.MARKETING_SITE_URL}{settings.OAUTH_SUCCESS_PATH}"
        },
    )


def oauth_failure(args: FailureArgs) -> BoltResponse:
    return BoltResponse(
        status=args.suggested_status_code, body="Wordle could not be installed."
    )


oauth_settings = OAuthSettings(
    client_id=settings.SLACK_CLIENT_ID,
    client_secret=settings.SLACK_CLIENT_SECRET,
    scopes=SCOPES,
    installation_store=FileInstallationStore(base_dir=settings.SLACK_INSTALLATIONS_DIR),
    install_page_rendering_enabled=False,
    state_store=FileOAuthStateStore(
        expiration_seconds=settings.SLACK_OAUTH_STATE_EXPIRATION,
        base_dir=settings.SLACK_OAUTH_STATE_DIR,
    ),
    callback_options=CallbackOptions(success=oauth_success, failure=oauth_failure),
)

app = App(signing_secret=settings.SLACK_SIGNING_SECRET, oauth_settings=oauth_settings)
