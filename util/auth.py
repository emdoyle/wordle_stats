from slack_bolt import App


def force_client_auth(app: "App", team_id: str):
    if app.installation_store is None:
        return
    app.client.token = app.installation_store.find_installation(
        enterprise_id=None, team_id=team_id
    ).bot_token
