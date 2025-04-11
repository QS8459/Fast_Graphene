from src.conf.log import logger
import graphene
from src.api.v1.account import (
    AccountBaseGraph,
    AccountInput,
    AddAccount,
    VerifyUser,
    TokenBaseGraph
)


class Query(
    graphene.ObjectType,
):
    account = graphene.Field(
        AccountBaseGraph,
        resolver=AccountBaseGraph.resolve_account,
        email=graphene.String()
    )
    account_list = graphene.Field(
        graphene.List(AccountBaseGraph),
        offset=graphene.Int(),
        limit=graphene.Int(),
        resolver=AccountBaseGraph.resolve_account_list
    )
    token = graphene.Field(
        TokenBaseGraph
    )
    hello = graphene.String(name=graphene.String())

    async def resolve_hello(root, info, name: str = "Name"):
        return f"Hello"+ name


class Mutation(graphene.ObjectType):
    add_account = AddAccount.Field()
    verify_account = VerifyUser.Field()



