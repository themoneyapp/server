from typing import Union

from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.routing import Mount

from . import api


def use_route_names_as_operation_ids(app: Union[FastAPI, Mount]) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'

        elif isinstance(route, Mount) and route.routes is not None:
            use_route_names_as_operation_ids(route)


def setup_routes(app: FastAPI) -> None:
    api_router = api.get_router()

    app.include_router(api_router)

    use_route_names_as_operation_ids(app)
