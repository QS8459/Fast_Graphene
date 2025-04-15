from starlette_graphene3 import (
    GraphQLApp,
    make_graphiql_handler,
    make_playground_handler,
)
import graphene
from fastapi import (
    FastAPI,
    status,
    Request,
    HTTPException
)
from contextlib import asynccontextmanager
from fastapi.responses import (
    JSONResponse,
)
from src.db.engine import AsyncSession, get_session
from fastapi.middleware.cors import CORSMiddleware
from src.conf.log import logger
from src.conf.settings import settings
from src.conf.middleware import (
    provide_session,
    authentication_middleware
)
from src.api import (
    schema,
    api
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        logger.info("I STARTED IT")
        from src.conf.db_conf import engine
        yield
        await engine.dispose()
    except Exception as e:
        logger.error('Engine')

app = FastAPI(
    lifespan=lifespan,
    title=settings.app_title,
    version=settings.app_version,
    description=settings.app_description,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# app.middleware("http")(provide_session)
app.middleware('http')(authentication_middleware)


@app.get('/')
async def home():
    return JSONResponse(
        content="Welcome Home!",
        status_code=status.HTTP_200_OK
    )

app.include_router(api)

app.mount(
    '/graphql',
     GraphQLApp(
         schema=schema,
         # context=lambda: {"session": get_session()},
         # on_get=make_playground_handler(),
         on_get=make_graphiql_handler()
     )
)
