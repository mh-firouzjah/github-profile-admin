'''
asynchronous data reading from WakaTime rest-API using python aiohttp package
'''

import base64
from datetime import date
from typing import Literal

import aiohttp


class WakaTimeReader(object):
    '''
    Read data from WakaTime API

    the instance uses `API Key` to authenticate as a reader,
    as the intention is to just read data, not to write
    '''

    base_url = "https://wakatime.com/api/v1"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    @property
    def headers(self):
        base64_encoded_toke = base64.b64encode(
            self.api_key.encode('utf-8')).decode("utf-8")
        return {'Authorization': f'Basic {base64_encoded_toke}'}

    async def aiohttp_get(self, url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                return await response.json()

    async def read_stats(self, range: Literal['last_7_days', 'last_30_days',
                                              'last_6_months', 'last_year'] = 'last_7_days'):
        url = f"/users/current/stats/{range}"
        return await self.aiohttp_get(self.base_url+url)

    async def read_date_stats(self, date: date):
        url = f"/users/current/durations?date={date}"
        return await self.aiohttp_get(self.base_url+url)
