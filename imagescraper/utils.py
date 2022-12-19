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
from .exceptions import ParseException


def generate_google_request(action, query, cursor) -> str:
    """
    Generates request for google /batchexecute endpoint
    """
    request = dumps(
        [
            None, None, cursor['first_list'], None, None, None,
            None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None,
            None, None, None, None,
            [query, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None,
             None, None, None, "lnms", None, None, None, None, None,
             None, None, None, []], None, None, None, None, None, None,
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
    return loads(data, strict=False)


def parse_response(response) -> Tuple[list, dict]:
    """
    Parse the response from the search result.
    """
    results = []
    cursor = {}
    for data in response:
        if isinstance(data, list):
            for total in data:
                if isinstance(total, list):
                    if len(total) > 0:
                        for container in total:
                            if isinstance(container, list):
                                if isinstance(container[0], list) and (len(container[0]) > 1):
                                    outer_holder = container[0]
                                    cursor_holder = next(
                                        iter(outer_holder[0][0].values()))
                                    search_result_holder = outer_holder[1][0]

                                    for cursor_list in cursor_holder:
                                        if isinstance(cursor_list, list):
                                            if 'GRID_STATE0' in cursor_list:
                                                for cursor_item in cursor_list:
                                                    if isinstance(cursor_item, list):
                                                        if len(cursor_item) > 1:
                                                            if isinstance(cursor_item[0], bool):
                                                                cursor.update(
                                                                    {'second_list': cursor_item[2:]})
                                                            elif isinstance(cursor_item[0], int):
                                                                cursor.update(
                                                                    {'first_list': cursor_item})
                                                break

                                    for search_item in search_result_holder:
                                        search_data = next(
                                            iter(search_item[0][0].values()))

                                        if isinstance(search_data[1], list):
                                            last_index = len(search_data[1]) - 1
                                            results.append(SearchResult(
                                                search_data[1][last_index]['2003'][3], search_data[1][3][0],
                                                search_data[1][last_index]['2003'][2], search_data[1][2][0]))

    if len(results) == 0:
        raise ParseException('No results found')

    if cursor == {}:
        raise ParseException('Cursor not found')

    return results, cursor
