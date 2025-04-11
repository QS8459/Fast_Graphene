from fastapi import Depends
from src.core.service.account import get_account_service, AccountService


async def get_graphql_context(
        account_service: AccountService = Depends(get_account_service)
) -> dict:
    return {
        "account_service": account_service
    }