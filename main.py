import argparse

import uvicorn
from fastapi import FastAPI

from src.api.events.database import on_shutdown, on_startup
from src.core.config import get_app_settings
from src.core.settings import AppSettings


def get_application(settings: AppSettings) -> FastAPI:
    application = FastAPI(**settings.fastapi_kwargs)

    application.add_event_handler(
        "startup",
        on_startup(application, settings),
    )
    application.add_event_handler(
        "shutdown",
        on_shutdown(application),
    )

    return application


parser = argparse.ArgumentParser()
parser.add_argument("--app_type", type=str, default="dev")
args = parser.parse_args()
app_settings = get_app_settings(args.app_type)
app = get_application(app_settings)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)
