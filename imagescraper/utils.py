from json import loads, dumps
from .abc import SearchResult


def generate_google_request(action, query, cursor):
    """
    Generates request for google /batchexecute endpoint
    """
    request = dumps(
        [
            None, None, cursor['first_list'], None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            [query], None, None, None, None, None, None, None, None, cursor['second_list'], None, False
        ]
    )
    request = request.replace('\\', '\\\\')
    request = request.replace('"', '\\"')
    request = '[[["{0}","{1}",null,"generic"]]]'.format(action, request)

    return request


def parse_google_json(data):
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
    data = data[21:]
    data = data[:-28]
    return loads(data)


def parse_data(data):
    """
    Parse the data from the search result.
    """
    results = []
    cursor = {}
    if isinstance(data, list):
        if len(data) == 1:
            if 'b-GRID_STATE0' in data[0]:
                for inside_data in data[0]:
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
                                                            item[1][9]['2003'][3], item[1][3][0], item[1][9]['2003'][2], item[1][2][0]))
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
    return results, cursor
