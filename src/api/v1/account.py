import graphene
from src.core.service.account import AccountService
from src.conf.di import di
from src.conf.log import logger
from src.core.service.authentication import generate_token
from src.conf.settings import settings
from src.api.v1.token import TokenBaseGraph
from src.core.interface import BaseInterface


class AccountBaseGraph(graphene.ObjectType):
    class Meta:
        interfaces = (BaseInterface,)

    email = graphene.String()
    account = graphene.String(
        email=graphene.String()
    )

    async def resolve_account(
            root,
            info,
            email: str = None,
            service: AccountService = di.resolve(AccountService)
    ):
        result = await service.get_by_email(
            email=email
        )
        return AccountBaseGraph(
            guid=result.guid,
            email=result.email
        )

    async def resolve_account_list(
            root,
            info,
            offset: int,
            limit: int,
            service: AccountService = di.resolve(AccountService)
    ):
        result = await service.get_all(
            offset=offset - 1,
            limit=limit
        )
        return result


class AccountInput(graphene.InputObjectType):

    email = graphene.String(required=True)
    password = graphene.String(required=True)


class AddAccount(graphene.Mutation):

    class Arguments:
        account_data = AccountInput(required=True)

    account = graphene.Field(AccountBaseGraph)

    async def mutate(
            self,
            info,
            account_data,
            service: AccountService = di.resolve(AccountService)
    ):
        logger.info(f"{account_data}")
        new_account = await service.add(
            **account_data
        )
        return AddAccount(
            account=AccountBaseGraph(
                guid=new_account.guid,
                email=new_account.email
            )
        )


class VerifyUser(graphene.Mutation):

    class Arguments:
        account_data = AccountInput(required=True)

    token = graphene.Field(TokenBaseGraph)

    async def mutate(
            root,
            info,
            account_data,
            service: AccountService = di.resolve(AccountService)
    ):
        user = await service.verify_account(
            email=account_data.email,
            password=account_data.password
        )
        access_token = await generate_token(
            {
                "username": user.email,
                "guid": str(user.guid),
            },
            exp_time=settings.token_exp_time_sec
        )
        refresh_token = await generate_token(
            {
                "username": user.email,
                "guid": str(user.guid),
            },
            exp_time=settings.refresh_token_exp_time_sec
        )
        logger.info(
            refresh_token
        )
        return VerifyUser(
            token=TokenBaseGraph(
                access_token=access_token,
                refresh_token=refresh_token
            )
        )

