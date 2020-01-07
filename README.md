# Django를 이용한 REST API
- Django REST Framework을 이용하지 않고 REST API를 구현
- REST API에 대한 동작 구조 이해



### Django를 이용한 REST API

- Serialize: Django 모델 객체를 Json 타입으로 직렬화
  - 데이터가 패킷에 담겨 전송되기 위해 Json은 binary 형태로 변환되어야 한다.
- json.loads: json(binary) 데이터를 python 데이터로 변환
- json.dumps: python 데이터를 json(binary)로 변환
- [django.core.serializers.serialize]: django에서 제공하는 직렬화 클래스

**[Mixin](https://github.com/navill/pure_restapi/tree/master/src/updates/api#mixin)**

**[Model](https://github.com/navill/pure_restapi/tree/master/src/updates#model)**

**[View](https://github.com/navill/pure_restapi/tree/master/src/updates/api#view)**

- GET
- PUT
- DELETE