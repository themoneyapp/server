from fastapi.routing import APIRouter
from starlette.responses import JSONResponse

from . import api_v1
from app.core.config import settings


def get_router() -> APIRouter:
    router = APIRouter(
        include_in_schema=True,
        default_response_class=JSONResponse,
        prefix=settings.API_PREFIX,
    )

    # Include v1 endpoints
    router.include_router(api_v1.get_router(), prefix=settings.API_V1_STR)

    return router
