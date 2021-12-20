import unittest
import asyncio
import imagescraper


class ScrapeTest(unittest.TestCase):
    """Check if it can scrape google images"""

    def setUp(self) -> None:
        async def setup_function():
            return imagescraper.GoogleScraper()
        self.loop = asyncio.new_event_loop()
        self.scraper = self.loop.run_until_complete(setup_function())

    def test_scrape(self):
        async def scrape_function():
            return await self.scraper.scrape("test", amount=100)
        result = self.loop.run_until_complete(scrape_function())
        self.assertTrue(len(result) == 100)

    def test_scrape_many(self):
        async def scrape_function():
            return await self.scraper.scrape("test", amount=200)
        result = self.loop.run_until_complete(scrape_function())
        self.assertTrue(len(result) == 200)

    def tearDown(self) -> None:
        async def close_function():
            await self.scraper.close()
        print('sus')
        try:
            self.loop.run_until_complete(close_function())
        finally:
            self.loop.close()

        del self.scraper
        del self.loop
