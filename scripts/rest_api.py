import os
import requests
import json
ENDPOINT = f"http://127.0.0.1:8000/api/status/"
image_path = os.path.join(os.getcwd(), 'django-icon-0.jpg')
headers = {
    'Content-Type': 'application/json',
}

user_data = {
    'username': 'jihoon',
    'password': 'gkdl1493',
}


# json 데이터를 이용할 경우(application/json) 반드시 json.dumps로 전달
def get_token(headers, user_data):
    endpoint = "http://127.0.0.1:8000/api/auth/"
    r = requests.post(endpoint, data=json.dumps(user_data), headers=headers)
    token = r.json()['token']
    print(token)
    return token


# 로그인 후 토큰 획득
# token = get_token(headers, user_data)


##################################################################################
def update_with_image(token, image_path, id):
    endpoint = f"http://127.0.0.1:8000/api/status/{id}/"
    headers = {
        # 'Content-Type': 'application/json',
        'Authorization': 'JWT ' + token,
    }
    data = {
        'content': 'this new content post'
    }
    # script 폴더 내에 이미지가 있어야 한다.
    with open(image_path, 'rb') as image:
        file_data = {
            # serializer field
            'image': image
        }
        # data는 raw(JSON이 아닌 python 데이터 타입)데이터를 사용한다.
        r = requests.put(endpoint, data=data, headers=headers, files=file_data)
        print(r.text)


# 컨텐츠 + 이미지 업데이트(put)
# update_with_image(token, image_path, 28)


# token = r.json()  # ['token']

##########################################################################

def do_refresh_token(endpoint=ENDPOINT):
    auth_endpoint = "http://127.0.0.1:8000/api/auth/register/"
    refresh_endpoint = "http://127.0.0.1:8000/api/auth/jwt/refresh/"

    headers = {
        'Content-Type': 'application/json',
    }

    auth_headers = {
        "Content-Type": "application/json",
        "Authorization": "JWT " + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6ImppaG9vbiIsImV4cCI6MTU4MzY5Mjg2MiwiZW1haWwiOiJqaWhvb25AbmF2ZXIuY29tIiwib3JpZ19pYXQiOjE1ODM2OTI1NjJ9.wT07v1iSXxbI_jWI74eAvinceJt4vfXEWPOB3LCYZug',
    }

    data = {
        'username': 'ddddl2ads5dfd132',
        'email': '53dd2@naver.com',
        'password': '1234',
        'password2': '1234',
    }

    data_content = {
        'content': 'this new content post'
    }
    # json 데이터를 이용할 경우(application/json) 반드시 json.dumps로 전달 - 회원가입 후 토큰 획득
    r = requests.post(auth_endpoint, data=json.dumps(data), headers=headers)
    token = r.json()['token']
    print(token)

    refresh_token = {
        'token': str(token)
    }
    # token 값 변경
    import time
    time.sleep(2)
    r = requests.post(refresh_endpoint, data=json.dumps(refresh_token), headers=headers)
    print(r.json())


do_refresh_token()


# image upload test
def upload_image(headers, user_data, endpoint=ENDPOINT):

    headers = {
        # "Content-Type": "application/json",
        "Authorization": "JWT " + get_token(headers, user_data),
    }

    with open(image_path, 'rb') as image:
        file_data = {
            # serializer field
            'image': image
        }

        post_data = {'content': 'some random content'}  # json.dumps({'content': 'some random content'})
        posted_response = requests.post(endpoint, data=post_data, headers=headers, files=file_data)

        print(posted_response.text)

# upload_image(headers, user_data)

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


def image_do(method='get', data={}, is_json=True, img_path=None, endpoint=ENDPOINT):
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
            r = requests.request(method, endpoint, data=data, files=file_data)
    else:
        r = requests.request(method, endpoint, data=data, headers=headers)
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
