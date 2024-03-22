from fastapi import FastAPI

from app.api.events.database import on_shutdown, on_startup
from app.core.config import get_app_settings
from app.core.settings import AppTypeSettings


def get_application() -> FastAPI:
    """Returning application by settings"""

    app_type = AppTypeSettings().type
    settings = get_app_settings(app_type)

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


app = get_application()
