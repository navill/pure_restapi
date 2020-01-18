import requests
import json

BASE_URL = 'http://127.0.0.1:8000/'
ENDPOINT = 'http://127.0.0.1:8000/api/status/'

get_endpoint = ENDPOINT + str(14)
post_data = json.dumps({'content': 'Some random content'})

r = requests.get(get_endpoint)
print(r.text)
r2 = requests.get(ENDPOINT)
print(r2.status_code)

post_headers = {
    'content-type': 'application/json',
}

post_response = requests.post(ENDPOINT, data=post_data, headers=post_headers)
print(post_response.text)  # authentication error


def get_list(id=None):  # --> list
    data = json.dumps({})
    if id is not None:
        data = json.dumps({'id': id})  # -> retrieve
    r = requests.get(BASE_URL + ENDPOINT, data=data)
    data = r.json()
    # print(r.status_code)  # 200
    # print(type(json.dumps(data)))  # <class 'str'>
    # for obj in data:
    #     # print(obj['id'])
    #     if obj['id'] == 1:  # detail
    #         r2 = requests.get(BASE_URL + ENDPOINT + str(obj['id']))
    #         # print(dir(r2))
    #         # print(r2.json())
    return data


# print(get_list())
# get_list()


# UpdateListAPIView 실행
def create_update():
    # 장고 내에서 익명의 유저로 Update 객체를 생성하려고 하기 때문에 에러를 일으킨다.
    # -> csrf_exam
    new_data = {
        'id': 7,
        'user': 1,
        'text': 'Another cool contents'
    }
    r = requests.post(BASE_URL + ENDPOINT, data=json.dumps(new_data))
    print(r.status_code)
    if r.status_code == requests.codes.ok:
        print(r.json())
        return r.json()
    return r.text


# print(get_list())


# print(create_update())


def obj_update():
    # 장고 내에서 익명의 유저로 Update 객체를 생성하려고 하기 때문에 에러를 일으킨다.
    # -> csrf_exam
    new_data = {
        'id': 11,
        'text': 'new changed obj data'
    }
    # r = requests.put(BASE_URL + ENDPOINT + '1', data=new_data)
    # -> {"message": "Invalid data sent, please send using JSON."}
    r = requests.put(BASE_URL + ENDPOINT, data=json.dumps(new_data))
    # -> {'message': 'something'}
    # new_data = {
    #     'id': 1,
    #     'text': 'Another cool contents'
    # }
    # r = requests.post(BASE_URL + ENDPOINT, data=new_data)
    # print(r.json())
    # print(r.headers)
    print(r.status_code)
    if r.status_code == requests.codes.ok:
        print(r.json())
        return r.json()
    return r.text


def obj_delete():
    # 장고 내에서 익명의 유저로 Update 객체를 생성하려고 하기 때문에 에러를 일으킨다.
    # -> csrf_exam
    new_data = {
        'id': 11
        # 'text': 'new obj data'
    }
    r = requests.delete(BASE_URL + ENDPOINT, data=json.dumps(new_data))
    print(r.status_code)
    if r.status_code == requests.codes.ok:
        # print(r.json())
        return r.json()
    return r.text

# print(obj_update())
# print(obj_delete())
