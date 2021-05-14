from setuptools import setup

req = []
with open('requirements.txt') as f:
    req = f.read().splitlines()

setup(
    name='google-image-scraper',
    author='Alpha-1004',
    url='https://github.com/Alpha-1004/google-image-scraper',
    version='1.0.0',
    packages=['imagescraper'],
    license='MIT',
    description='Google image scraper is a tool to scrape images from google.',
    include_package_data=True,
    install_requires=req,
    python_requires='>=3.7.0'
)