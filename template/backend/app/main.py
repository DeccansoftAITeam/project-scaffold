"""FastAPI entry point. Routers only wire HTTP to feature services: no business logic here."""

from fastapi import FastAPI

from app.core import errors, telemetry
from app.core.config import get_settings
from app.core.input_guard import RejectNul
from app.features.health.router import router as health_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        responses=errors.PROBLEM_RESPONSES,  # every error status documented as RFC 7807
        redirect_slashes=False,  # /items/ must 404, not silently become another route
    )
    errors.install(app)
    app.add_middleware(RejectNul)  # Postgres text can't hold U+0000: 422, not 500
    telemetry.install(app, settings)
    app.include_router(health_router)
    return app


app = create_app()
