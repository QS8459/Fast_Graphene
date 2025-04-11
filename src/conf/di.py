from typing import (
    Type,
    TypeVar,
    Generic,
    Callable,
    Dict,
    Any,
    AsyncGenerator,
    Coroutine
)
from asyncio import run
from src.conf.log import logger

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class DependencyContainer(Generic[T]):

    def __init__(self, ):
        self._dependency: Dict[Type, Callable[[], Any]] = {}
        self._async_dependency: Dict[Type, Callable[[], Coroutine[Any, Any, Any]]] = {}

    def register(self, interface: Type[T], implementation: Callable[[], T]):
        self._dependency[interface] = implementation

    def register_async(
            self,
            interface: Type[T],
            implementation: Callable[[], Coroutine[Any, Any, T]]
    ):
        self._async_dependency[interface] = implementation

    async def async_resolver(self, interface: Type[T]) -> T:
        if interface not in self._async_dependency:
            raise ValueError(f"Async dependency {interface} is not registered")
        async for a in self._async_dependency[interface]():
            return a

    def resolve(self, interface: Type[T]) -> T:
        if interface in self._async_dependency:
            return run(self.async_resolver(interface))
        if interface not in self._dependency:
            raise ValueError(f"Dependency {interface} is not registered")

        return self._dependency[interface]()


di = DependencyContainer()
