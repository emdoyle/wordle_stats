from app.apps import app


@app.event("app_home_opened")
def handle_app_home_opened():
    ...
