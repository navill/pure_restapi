import os

import requests
import json

AUTH_ENDPOINT = "http://127.0.0.1:8000/api/auth/"
REFRESH_ENDPOINT = "http://127.0.0.1:8000/api/auth/jwt/refresh/"

# script 폴더 내에 이미지가 있어야 한다.
image_path = os.path.join(os.getcwd(), 'django-icon-0.jpg')

headers = {
    'Content-Type': 'application/json',
}

data = {
    'username': 'jihoon',
    'password': 'gkdl1493',
}
# json 데이터를 이용할 경우(application/json) 반드시 json.dumps로 전달
r = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)
token = r.json()['token']
print(token)

ENDPOINT = "http://127.0.0.1:8000/api/status/29/"
headers2 = {
    # 'Content-Type': 'application/json',
    'Authorization': 'JWT ' + token,
}
data2 = {
    'content': 'this new content post'
}

with open(image_path, 'rb') as image:
    file_data = {
        # serializer field
        'image': image
    }
    r = requests.put(ENDPOINT, data=data2, headers=headers2, files=file_data)
    print(r.text)









# token = r.json()  # ['token']


# AUTH_ENDPOINT = "http://127.0.0.1:8000/api/auth/register/"
# REFRESH_ENDPOINT = "http://127.0.0.1:8000/api/auth/jwt/refresh/"
# ENDPOINT = "http://127.0.0.1:8000/api/status/"
# # script 폴더 내에 이미지가 있어야 한다.
# image_path = os.path.join(os.getcwd(), 'django-icon-0.jpg')
#
# headers = {
#     'Content-Type': 'application/json',
# }
#
# auth_headers = {
#     "Content-Type": "application/json",
#     "Authorization": "JWT " + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNywidXNlcm5hbWUiOiJqM2QxYWRzZGYzZGRkMzIiLCJleHAiOjE1NzkzNTUwNjUsImVtYWlsIjoiamgxM2RkYWRzZmQzMkBuYXZlci5jb20iLCJvcmlnX2lhdCI6MTU3OTM1NDc2NX0.4sPIWgy3vv0SsQRyA_FUIxpjvwo8wOxOWwkNYo1tOeM',
# }
#
# data = {
#     'username': 'j3d1adsdf3dddd32',
#     'email': 'jh13ddaddsfd32@naver.com',
#     'password': 'gkdl1493',
#     'password2': 'gkdl1493',
# }
# # json 데이터를 이용할 경우(application/json) 반드시 json.dumps로 전달
# r = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=auth_headers)
# token = r.json()  # ['token']
# print(token)


# refresh_token = {
#     'token': token
# }
#
# r = requests.post(REFRESH_ENDPOINT, data=json.dumps(refresh_token), headers=headers)
# print(r.json())

# image upload test
# headers = {
#     # "Content-Type": "application/json",
#     "Authorization": "JWT " + token,
# }
#
# with open(image_path, 'rb') as image:
#     file_data = {
#         # serializer field
#         'image': image
#     }
#
#     post_data = {'content': 'some random content'}  # json.dumps({'content': 'some random content'})
#     posted_response = requests.post(ENDPOINT, data=post_data, headers=headers, files=file_data)
#
#     print(posted_response.text)
#
# # put test
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "JWT " + token,
# }
# data = {
#     "content": "update description"
# }
# json_data = json.dumps(data)
# posted_response = requests.put(ENDPOINT+str(23)+'/', data=json_data, headers=headers)
# print(posted_response.text)


def image_do(method='get', data={}, is_json=True, img_path=None):
    headers = {}

    if is_json:
        headers['content-type'] = 'application/json'
        data = json.dumps(data)
    if img_path is not None:
        with open(image_path, 'rb') as image:
            file_data = {
                # serializer field
                'image': image
            }
            r = requests.request(method, ENDPOINT, data=data, files=file_data)
    else:
        r = requests.request(method, ENDPOINT, data=data, headers=headers)
    print(r.text)
    print(r.status_code)
    return r


# image_do(method='post', data={'user': 2, 'content': 'image'}, is_json=False, img_path=image_path)
# image_do(method='put', data={'id': 17, 'user': 2, 'content': 'change content and image'}, is_json=False,
#          img_path=image_path)


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
# do(method='delete', data={'id': 11})
# do(method='post', data={'content': 'new item!!', 'user': 2})
