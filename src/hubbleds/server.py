import os
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route
from solara.server import settings

import solara.server.starlette


# Check if we need to run in demo mode
force_demo = os.getenv("CDS_FORCE_DEMO", "false").strip().lower() == "true"


def root(request: Request):
    return JSONResponse({"Error Message": "Go back whence ye came."})


if force_demo:
    routes = [
        Mount("/", routes=solara.server.starlette.routes),
    ]
else:
    routes = [
        Route("/", endpoint=root),
        Mount("/hubbles-law/", routes=solara.server.starlette.routes),
    ]


app = Starlette(routes=routes, middleware=solara.server.starlette.middleware)
