from environs import Env

env = Env()

env.read_env()

SLACK_SIGNING_SECRET = env.str("SLACK_SIGNING_SECRET")
SLACK_BOT_TOKEN = env.str("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = env.str("SLACK_APP_TOKEN")
