from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from status.api.serializers import StatusSerializer
from status.models import Status

# serializer single object
obj = Status.objects.first()
serializer = StatusSerializer(obj)
json_data = JSONRenderer().render(serializer.data)
print(json_data)

stream = BytesIO(json_data)
data = JSONParser().parse(stream)
print(data)

# serializer queryset
qs = Status.objects.all()
qs_serializer = StatusSerializer(qs, many=True)
qs_json_data = JSONRenderer().render(qs_serializer.data)
print(qs_json_data)

qs_stream = BytesIO(qs_json_data)
qs_data = JSONParser().parse(qs_stream)
print(qs_data)

# create obj
data = {'user': 2}
# 유효성 검사가 일어나지 않은 데이터는 data키워드 인자에 담는다.
serializer = StatusSerializer(data=data)
# save 전 반드시 is_valid
serializer.is_valid()  # validation => True
serializer.save()

# if serializer.is_valid():
#     serializer.save()

# update obj
obj = Status.objects.first()
data = {'user': 2, 'content': 'some new content!!!!!!!!!!'}
update_serializer = StatusSerializer(obj, data=data)
update_serializer.is_valid()
update_serializer.save()

# delete obj
obj = Status.objects.first()
data = {'user': 2, 'content': 'please delete me'}
create_obj_serializer = StatusSerializer(obj, data=data)
create_obj_serializer.is_valid()
create_obj = create_obj_serializer.save()  # return instance of object
print(create_obj.id)  # 1

obj = Status.objects.last()
# delete_serializer = StatusSerializer(obj)
obj.delete()