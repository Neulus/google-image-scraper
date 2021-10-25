import aiohttp
import demjson
import re


class GoogleScraper:
    """Google Image Scrapper"""

    def __init__(self, host='https://google.com') -> None:
        self.host = host
        self._session = aiohttp.ClientSession(
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})

        self.af_data_regex = re.compile(
            r"AF_initDataCallback\({key: 'ds:1'(.|\n)*?}}")

    async def close(self):
        """Closes aiohttp session"""
        await self._session.close()

    async def scrape(self, query: str, safe_search=False) -> list:
        """Scrapes image from google"""
        url = '{0}/search?q={1}&tbm=isch'.format(
            self.host, query + '&safe=active' if safe_search else query)
        site = await self._session.get(url)
        if site.status != 200:
            raise Exception('Google is weird today')
        site_data = await site.text()

        af_data_result = self.af_data_regex.search(site_data)

        af_string = af_data_result.group(0).replace(
            'AF_initDataCallback', '').strip('()')
        af_data = demjson.decode(af_string)
        result = []

        for data in af_data['data']:
            if isinstance(data, list):
                if len(data) == 1:
                    if 'b-GRID_STATE0' in data[0]:
                        for inside_data in data[0]:
                            if isinstance(inside_data, list):
                                if 'GRID_STATE0' in inside_data:
                                    for outer_item in inside_data:
                                        if isinstance(outer_item, list):
                                            if len(outer_item) > 0:
                                                for item in outer_item:
                                                    if isinstance(item, list):
                                                        if len(item) > 5:
                                                            if isinstance(item[0], int) and isinstance(item[1], list):
                                                                result.append({
                                                                    'preview_image': item[1][2][0],
                                                                    'image_url': item[1][3][0],
                                                                    'title': item[1][9]['2003'][3],
                                                                    'url': item[1][9]['2003'][2]
                                                                })
                        break
        return result
