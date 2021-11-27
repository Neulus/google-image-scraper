""""
The MIT License (MIT)
Copyright (c) 2021-present Alpha-1004
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from setuptools import setup

req = []
with open('requirements.txt') as f:
    req = f.read().splitlines()

setup(
    name='google-image-scraper',
    author='Alpha-1004',
    url='https://github.com/Alpha-1004/google-image-scraper',
    version='2.0.1',
    packages=['imagescraper'],
    license='MIT',
    description='Google image scraper is a tool to scrape images from google.',
    include_package_data=True,
    install_requires=req,
    python_requires='>=3.7.0'
)
