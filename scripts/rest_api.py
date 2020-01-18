import requests
import json

ENDPOINT = "http://127.0.0.1:8000/api/status/"


def do(method='get', data={}, is_json=True):
    # json 타입으로 요청할 경우 header의 content-type을 설정하고 요청에 포함시켜야 한다.
    # {"detail":"Unsupported media type \"text/plain\" in request."} 에러
    headers = {}

    if is_json:
        headers['content-type'] = 'application/json'
        data = json.dumps(data)
    r = requests.request(method, ENDPOINT, data=data, headers=headers)
    print(r.text)
    print(r.status_code)
    return r


# do(data={'id': 500}) # -> not found - 404
# r = requests.request('get', ENDPOINT + '?id=5', data={'id': 5})
do(method='delete', data={'id': 11})
do(method='post', data={'content': 'new item!!', 'user': 2})
