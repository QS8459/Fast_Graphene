import graphene
from src.api.v1 import Query, Mutation

schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)

