from fastapi import APIRouter

from .endpoints import auth, users, utils


def get_router() -> APIRouter:
    router = APIRouter()

    router.include_router(auth.router, tags=["Auth"])
    router.include_router(users.router, prefix="/users", tags=["Users"])
    router.include_router(utils.router, prefix="/utils", tags=["Utils"])

    return router
