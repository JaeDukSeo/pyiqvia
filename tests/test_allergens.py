"""Define tests for the "Allergens" object."""
# pylint: disable=redefined-outer-name,unused-import

import json

import aiohttp
import pytest

from pyiqvia import Client
from pyiqvia.errors import InvalidZipError

from .const import TEST_BAD_ZIP, TEST_ZIP
from .fixtures.allergens import *  # noqa


@pytest.mark.asyncio
async def test_current(aresponses, event_loop, fixture_current):
    """Test getting current allergen data."""
    aresponses.add(
        'www.pollen.com',
        '/api/forecast/current/pollen/{0}'.format(TEST_ZIP), 'get',
        aresponses.Response(text=json.dumps(fixture_current), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TEST_ZIP, websession)

        current = await client.allergens.current()
        assert len(current['Location']['periods']) == 3


@pytest.mark.asyncio
async def test_extended(aresponses, event_loop, fixture_extended):
    """Test getting extended allergen info."""
    aresponses.add(
        'www.pollen.com', '/api/forecast/extended/pollen/{0}'.format(TEST_ZIP),
        'get',
        aresponses.Response(text=json.dumps(fixture_extended), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TEST_ZIP, websession)

        extended = await client.allergens.extended()
        assert len(extended['Location']['periods']) == 5


@pytest.mark.asyncio
async def test_historic(aresponses, event_loop, fixture_historic):
    """Test getting historic allergen info."""
    aresponses.add(
        'www.pollen.com', '/api/forecast/historic/pollen/{0}'.format(TEST_ZIP),
        'get',
        aresponses.Response(text=json.dumps(fixture_historic), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TEST_ZIP, websession)

        historic = await client.allergens.historic()
        assert len(historic['Location']['periods']) == 30


@pytest.mark.asyncio
async def test_outlook(aresponses, event_loop, fixture_outlook):
    """Test getting outlook allergen info."""
    aresponses.add(
        'www.pollen.com', '/api/forecast/outlook/{0}'.format(TEST_ZIP), 'get',
        aresponses.Response(text=json.dumps(fixture_outlook), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TEST_ZIP, websession)

        outlook = await client.allergens.outlook()
        assert outlook['Trend'] == 'subsiding'


@pytest.mark.asyncio
async def test_bad_zip(aresponses, event_loop, fixture_empty_response):
    """Test the cases that would arise from a bad ZIP code."""
    aresponses.add(
        'www.pollen.com',
        '/api/forecast/current/pollen/{0}'.format(TEST_BAD_ZIP), 'get',
        aresponses.Response(
            text=json.dumps(fixture_empty_response), status=200))
    aresponses.add(
        'www.pollen.com', '/api/forecast/outlook/{0}'.format(TEST_BAD_ZIP),
        'get', aresponses.Response(text='', status=404))

    with pytest.raises(InvalidZipError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(TEST_BAD_ZIP, websession)
            await client.allergens.current()

    with pytest.raises(InvalidZipError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(TEST_BAD_ZIP, websession)
            await client.allergens.outlook()
