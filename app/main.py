from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes import setup_routes


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_PATH}/openapi.json"
    )

    # Set all CORS enabled origins
    if settings.CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    setup_routes(app)

    return app


app = create_application()
