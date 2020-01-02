import json

from django.conf import settings
from django.contrib.gis import views
from django.core.serializers import serialize
from django.db import models


def upload_update_image(instance, filename):
    return f'updates/{instance.user}/{filename}'


class UpdateQuerySet(models.QuerySet):
    # def serialize(self):
    #     qs = self
    #     return serialize('json', qs, fields=('user', 'content', 'image'))
    # 오버라이딩 메소드
    def serialize(self):
        # QuerySet.values(<fields>)
        list_values = list(self.values('id', 'user', 'text', 'image'))
        # final_array = []
        # for obj in list_values:
        #     # 직렬화된 데이터를 python type으로 변환
        #     struct = json.loads(obj.serialize())  # django.core.serailizers.serialize
        #     final_array.append(struct)
        #     # dumps를 이용해 json type으로 변환
        return json.dumps(list_values)


class UpdateManager(models.Manager):
    def get_queryset(self):
        return UpdateQuerySet(self.model, using=self._db)


class Update(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_update_image, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now=True)

    objects = UpdateManager()

    def __str__(self):
        return self.text

    def serialize(self):
        # json_data = serialize('json', [self], fields=('user', 'text', 'image'))
        # struct = json.loads(json_data)
        # print(struct)
        # # output: {"user": 1, "text": "test", "image": ""}

        try:
            image = self.image.url
        except:
            image = ''
        data = {
            'id': self.id,
            'text': self.text,
            'user': self.user.id,
            'image': image,
        }

        data = json.dumps(data)
        return data
