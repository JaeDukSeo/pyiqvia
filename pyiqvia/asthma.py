"""Define an object to work with "Ashtma" endpoints."""
from typing import Awaitable, Callable

from .decorators import raise_on_invalid_zip


class Asthma:  # pylint: disable=too-few-public-methods
    """Define the "Asthma" object."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Initialize."""
        self._request = request

    @raise_on_invalid_zip
    async def current(self) -> dict:
        """Get current asthma info."""
        return await self._request(
            'get',
            'https://www.asthmaforecast.com/api/forecast/current/asthma')

    @raise_on_invalid_zip
    async def extended(self) -> dict:
        """Get extended asthma info."""
        return await self._request(
            'get',
            'https://www.asthmaforecast.com/api/forecast/extended/asthma')

    @raise_on_invalid_zip
    async def historic(self) -> dict:
        """Get historic asthma info."""
        return await self._request(
            'get',
            'https://www.asthmaforecast.com/api/forecast/historic/asthma')
