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
from json import loads, dumps
from typing import Tuple
from .abc import SearchResult


def generate_google_request(action, query, cursor) -> str:
    """
    Generates request for google /batchexecute endpoint
    """
    request = dumps(
        [
            None, None, cursor['first_list'], None, None,
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            [query], None, None, None, None, None, None,
            None, None, cursor['second_list'], None, False
        ]
    )
    request = request.replace('\\', '\\\\')
    request = request.replace('"', '\\"')
    request = '[[["{0}","{1}",null,"generic"]]]'.format(action, request)

    return request


def parse_google_json(data) -> list:
    """
    Converts Google's json to normal python list
    """
    data = data.replace('\\\\', '\\')
    data = data.replace('\\"', '"')
    data = data.replace('\\/', '/')
    data = data.replace('\\n', '\n')
    data = data.replace('\\t', '\t')
    data = data.replace('\\r', '\r')
    data = data.replace('\\b', '\b')
    data = data.replace('\\f', '\f')
    data = data[21:-28]
    return loads(data)


def parse_response(response) -> Tuple[list, dict]:
    """
    Parse the response from the search result.
    """
    results = []
    cursor = {}
    for data in response:
        if isinstance(data, list):
            for container in data:
                if isinstance(container, list):
                    if 'b-GRID_STATE0' in container:
                        for inside_data in container:
                            if isinstance(inside_data, list):
                                if 'GRID_STATE0' in inside_data:
                                    for outer_item in inside_data:
                                        if isinstance(outer_item, list):
                                            if len(outer_item) > 0:
                                                for item in outer_item:
                                                    if isinstance(item, list):
                                                        if len(item) > 5:
                                                            if isinstance(item[0], int) and isinstance(item[1], list):
                                                                results.append(SearchResult(
                                                                    item[1][9]['2003'][3], item[1][3][0],
                                                                    item[1][9]['2003'][2], item[1][2][0]))
                                                if isinstance(outer_item[0], bool):
                                                    cursor.update({
                                                        'second_list': outer_item[2:],
                                                    })
                                                elif isinstance(outer_item[0], int):
                                                    first_list = outer_item[:]
                                                    first_list[6] = []
                                                    first_list[7] = []
                                                    cursor.update({
                                                        'first_list': first_list,
                                                    })
                                    break

    return results, cursor
