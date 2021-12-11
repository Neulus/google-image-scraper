""""
The MIT License (MIT)
Copyright (c) 2021-present Neulus
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


class SearchResult:
    def __init__(self, title, image_url, url, preview_image) -> None:
        self.preview_image = preview_image
        self.image_url = image_url
        self.title = title
        self.url = url

    def __str__(self) -> str:
        return f"{self.image_url}"

    def __repr__(self) -> str:
        return f'<SearchResult image_url={self.image_url}>'

    def __hash__(self) -> int:
        return hash(self.image_url)

    def __eq__(self, other) -> bool:
        return self.image_url == other.image_url
