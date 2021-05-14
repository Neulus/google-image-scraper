# google-image-scraper
Google image scraper is a tool to scrape images from google. It uses aiohttp and regex to scrape original image, preview image, metadatas.
It can scrape images without selenium. The maximum amount you can scrape with it is 100.

> Warning : Abuse of this scraper can lead to your IP being banned by Google. (probably)

## Installation
```sh
$ git clone https://github.com/Alpha-1004/google-image-scraper
$ cd google-image-scraper

# MacOs/Linux
$ python3 -m pip install .
# Windows
$ py -m pip install .
```

## Example
```py
import asyncio
from imagescraper import GoogleScraper

async def main():
    scraper = GoogleScraper()
    for i in (await scraper.scrape('hi')):
        print(i)
    await scraper.close()

asyncio.run(main())
```

However, This project was originally created for my personal project.
