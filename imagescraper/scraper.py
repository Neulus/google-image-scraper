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
                    meta_string = af_string[i+3][af_string[i+3].find('http')-1:]
                    url = meta_string[1:meta_string.find('",')]
                    title = meta_string[meta_string.find('","')+3: meta_string.find('",null')]
                    data.append({
                        'preview_image': json.loads(af_string[i-1][af_string[i-1].find('https://encrypted-tbn0.gstatic.com') - 2:])[0],
                        'image_url': json.loads(text[1:])[0],
                        'title': str(title),
                        'url': str(url)
                    })
            i += 1
        return data