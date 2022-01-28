from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

from . import settings
from .db import Base, engine

Base.metadata.create_all(engine)

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

oauth_settings = OAuthSettings(
    client_id=settings.SLACK_CLIENT_ID,
    client_secret=settings.SLACK_CLIENT_SECRET,
    scopes=SCOPES,
    installation_store=FileInstallationStore(base_dir=settings.SLACK_INSTALLATIONS_DIR),
    state_store=FileOAuthStateStore(
        expiration_seconds=settings.SLACK_OAUTH_STATE_EXPIRATION,
        base_dir=settings.SLACK_OAUTH_STATE_DIR,
    ),
)

app = App(signing_secret=settings.SLACK_SIGNING_SECRET, oauth_settings=oauth_settings)
