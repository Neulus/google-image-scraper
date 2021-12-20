# google-image-scraper
[![Updates](https://pyup.io/repos/github/Neulus/google-image-scraper/shield.svg)](https://pyup.io/repos/github/Neulus/google-image-scraper/)

Google image scraper is a tool to scrape images from google. It uses aiohttp and regex to scrape original image, preview image, metadatas.
It can scrape images without selenium.

> Warning : Abuse of this scraper can lead to your IP being banned by Google. (probably)

## Installation

```sh
$ git clone https://github.com/Neulus/google-image-scraper
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
    for i in (await scraper.scrape('hi', amount=300)):
        print(i)
    await scraper.close()

asyncio.run(main())
```

However, This project was originally created for my personal project.
