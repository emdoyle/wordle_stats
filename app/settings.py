from environs import Env

env = Env()

env.read_env()

DEBUG = env.bool("DEBUG", False)

DEV_SERVER_PORT = env.int("DEV_SERVER_PORT", 8000)

SLACK_SIGNING_SECRET = env.str("SLACK_SIGNING_SECRET", "")
SLACK_APP_TOKEN = env.str("SLACK_APP_TOKEN")
SLACK_CLIENT_ID = env.str("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = env.str("SLACK_CLIENT_SECRET")
SLACK_INSTALLATIONS_DIR = env.str("SLACK_INSTALLATIONS_DIR", "./data/installations")
SLACK_OAUTH_STATE_DIR = env.str("SLACK_OAUTH_STATE_DIR", "./data/states")
SLACK_OAUTH_STATE_EXPIRATION = env.int("SLACK_OAUTH_STATE_EXPIRATION", 600)
SLACK_INSTALL_PATH = env.str("SLACK_INSTALL_PATH", "/slack/install")
SLACK_OAUTH_REDIRECT_PATH = env.str(
    "SLACK_OAUTH_REDIRECT_PATH", "/slack/oauth_redirect"
)

DB_PATH = env.str("DB_PATH", "wordle.db")
