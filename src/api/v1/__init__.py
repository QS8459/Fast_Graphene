from src.conf.log import logger
from src.api.v1.union_example import (
    SearchResult,
    mock_data
)
import graphene
from src.api.v1.account import (
    AccountBaseGraph,
    AccountInput,
    SignUp,
    VerifyUser,
)


class Query(
    graphene.ObjectType,
):
    result = graphene.Field(SearchResult)
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
    hello = graphene.String(name=graphene.String())
    verify_user = graphene.Field(
        VerifyUser,
        password=graphene.String(),
        email=graphene.String(),
        resolver=VerifyUser.resolve_verify_user
    )
    async def resolve_hello(root, info, name: str = "Name"):
        return f"Hello"+ name

    async def resolve_result(_, info):
        return mock_data


class Mutation(graphene.ObjectType):
    sign_up = SignUp.Field()



