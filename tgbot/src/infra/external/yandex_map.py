from typing import (
    Any,
)

import aiohttp

from .exceptions import (
    InvalidKey,
    NothingFound,
    UnexpectedResponse,
)


class Client:
    __slots__ = ("api_key",)
    api_key: str

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def _request(self, address: str) -> Any:
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                url="https://geocode-maps.yandex.ru/1.x/",
                params={"format": "json", "apikey": self.api_key, "geocode": address},
            ) as response,
        ):
            if response.status == 200:
                a = await response.json()
                return a["response"]
            if response.status == 403:
                raise InvalidKey
            msg = f"status_code={response.status}, body={response.content}"
            raise UnexpectedResponse(msg)

    async def coordinates(self, address: str) -> tuple[str, str]:
        d = await self._request(address)
        data = d["GeoObjectCollection"]["featureMember"]

        if not data:
            msg = f'Nothing found for "{address}" not found'
            raise NothingFound(msg)

        coordinates = data[0]["GeoObject"]["Point"]["pos"]
        longitude, latitude = tuple(coordinates.split(" "))
        return longitude, latitude

    async def address(self, longitude: str | float, latitude: str | float) -> Any:
        response = await self._request(f"{longitude},{latitude}")
        data = response.get("GeoObjectCollection", {}).get("featureMember", [])

        if not data:
            msg = f'Nothing found for "{longitude} {latitude}"'
            raise NothingFound(msg)

        try:
            address_details = data[0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]
        except KeyError:
            return None

        try:
            locality = address_details["AdministrativeArea"]["Locality"]["LocalityName"]
        except KeyError:
            try:
                locality = address_details["AdministrativeArea"]["SubAdministrativeArea"]["Locality"]["LocalityName"]
            except KeyError:
                return None

        return locality
