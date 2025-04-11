from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import (
    IntegrityError,
    ArgumentError,
    SQLAlchemyError
)
from sqlalchemy.future import select
from typing import Generic, TypeVar, Type
from abc import ABC, abstractmethod
from fastapi import HTTPException
from src.conf.log import logger

T = TypeVar("T")


class ServiceBase(ABC, Generic[T]):

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def __handle_in_session(self, caller, refresh=False, *args, **kwargs):
        try:
            result = await caller(*args, **kwargs)
            await self.session.commit()
            if refresh:
                await self.session.refresh(result)
                return result
            return result
        except IntegrityError as e:
            logger.error("Integrity Error")
            raise SQLAlchemyError(
                code=500,
            )
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError, {e}")
            raise HTTPException(
                detail=f"SQLAlchemyError,{e}",
                status_code=500
            )

    async def _exec(self, caller, fetch_one=False, refresh=False, *args, **kwargs):
        result = await self.__handle_in_session(caller, refresh, *args, **kwargs)
        if refresh:
            return result
        if fetch_one:
            return  result.scalars().first()
        return result.scalars().all()

    @abstractmethod
    async def before_add(self, instance: Type[T], *args, **kwargs):
        pass

    async def add(self, *args, **kwargs):
        async def _add(*in_args, **in_kwargs):
            instance = self.model(**in_kwargs)
            await self.before_add(instance, *in_args, **in_kwargs)
            self.session.add(instance)
            return instance
        return await self._exec(_add, refresh=True, *args, **kwargs)

    async def get_all(
            self,
            offset: int = 0,
            limit: int = 10
    ):
        async def _get_all(_offset:int, _limit: int):
            query = select(self.model).offset(_offset).limit(_limit)
            return await self.session.execute(query)

        return await self._exec(_get_all, fetch_one=False, _offset=offset, _limit=limit)
