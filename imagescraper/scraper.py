import aiohttp, json, re

class GoogleScraper:
    """Google Image Scrapper"""
    def __init__(self, host = 'https://google.com') -> None:
        self.host = host 
        self._session = aiohttp.ClientSession(headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})

        self.af_data_regex = re.compile(r"AF_initDataCallback\({key: 'ds:1'(.|\n)*?}}")

    async def close(self):
        """Closes aiohttp session"""
        await self._session.close()

    async def scrape(self, query:str, safe_search = False) -> list:
        """Scrapes image from google"""
        url = '{0}/search?q={1}&tbm=isch'.format(self.host, query + '&safe=active' if safe_search else query)
        site = await self._session.get(url)
        if site.status != 200:
            raise Exception('Google is weird today')
        site_data = await site.text()

        af_data_result = self.af_data_regex.search(site_data)

        af_string = af_data_result.group(0).split('\n')

        data = []
        i = 0
        for text in af_string:
            if 'https://' in text:
                if 'gstatic.com' in af_string[i-1]:
                    metadata_payload = json.loads('{' + af_string[i+3][1:] + '}]}')['2003']
                    data.append({
                        'preview_image': json.loads(af_string[i-1][1:] + ']]')[1][2][0],
                        'image_url': json.loads(text[1:])[0],
                        'title': metadata_payload[3],
                        'url': metadata_payload[2]
                    })
            i += 1
        return data
