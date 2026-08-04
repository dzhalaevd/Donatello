from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from .adapters import AuthServicesProvider, ConfigProvider, SqlalchemyProvider


def create_container() -> AsyncContainer:
    return make_async_container(
        FastapiProvider(),
        ConfigProvider(),
        SqlalchemyProvider(),
        AuthServicesProvider(),
    )


__all__ = ("create_container",)
