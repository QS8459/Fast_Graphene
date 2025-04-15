from fastapi import APIRouter
from src.api.v1.token import token_api
import graphene
from src.api.v1 import Query, Mutation

schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)

api: APIRouter = APIRouter(prefix="/api")
api.include_router(token_api)
