import graphene
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core.service.base import ServiceBase
from src.db.models.account import Account
from src.db.engine import get_session
from src.conf.di import di


class AccountService(ServiceBase):
    def __init__(self, session):
        super().__init__(
            session=session,
            model=Account
        )

    async def before_add(self, instance: Account, *args, **kwargs):
        instance.set_pwd(kwargs.get('password'))

    async def get_by_email(self, email: str):
        async def _get_by_email(_email: str):
            query = select(self.model).where(self.model.email == _email)
            return await self.session.execute(query)

        result = await self._exec(_get_by_email, fetch_one=True, _email=email)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No User Found"
            )
        return result

    async def verify_account(self, *args, **kwargs):
        user = await self.get_by_email(kwargs.get("email"))
        if user.ver_pwd(kwargs.get('password')):
            return user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect email or password"
        )


def get_account_service(session: AsyncSession = di.resolve(AsyncSession)):
    return AccountService(session)


di.register(AccountService, get_account_service)
