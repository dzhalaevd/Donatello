from typing import Protocol

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import CommitError, RollbackError


class UnitOfWork(Protocol):
    async def commit(self) -> None:
        raise NotImplementedError

    async def rollback(self) -> None:
        raise NotImplementedError


class SQLAlchemyUoW(UnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as err:
            raise CommitError from err

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as err:
            raise RollbackError from err
