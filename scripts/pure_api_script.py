import requests
import json

BASE_URL = 'http://127.0.0.1:8000/'
ENDPOINT = 'api/updates/'


def get_list():  # --> list
    r = requests.get(BASE_URL + ENDPOINT)
    data = r.json()
    # print(r.status_code)  # 200
    # print(type(json.dumps(data)))  # <class 'str'>
    for obj in data:
        # print(obj['id'])
        if obj['id'] == 1:  # detail
            r2 = requests.get(BASE_URL + ENDPOINT + str(obj['id']))
            print(dir(r2))
            print(r2.json())
    return data


# print(get_list())

get_list()
