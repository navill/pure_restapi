import json

from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View

from config.mixin import JsonResponseMixin
from updates.models import Update


def update_model_detail_view(request):
    data = {
        'count': 1000,
        'content': 'some new content',
    }
    json_data = json.dumps(data)
    print(json_data)
    return JsonResponse(data)
    # return render(request, template, {'context':...})
    # return HttpResponse(get_template().render({}))


class JsonCVB(View):
    def get(self, request):
        data = {
            'count': 1000,
            'content': 'some new content',
        }
        json_data = json.dumps(data)
        print(json_data)
        return HttpResponse(json_data, content_type='application/json')
        # return JsonResponse(data)


class JsonCVB2(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs):
        data = {
            'count': 1000,
            'content': 'some new content',
        }
        return self.render_to_json_response(data)


class SerializerDetailView(View):
    def get(self, request, *args, **kwargs):
        obj = Update.objects.get(id=1)
        json_data = obj.serialize()
        return HttpResponse(json_data, content_type='application/json')


class SerializerListView(View):
    def get(self, request, *args, **kwargs):
        qs = Update.objects.all()
        json_data = qs.serialize()
        print(json_data)
        # HttpResponse(content=b'') -> json 타입 데이터를 매개 변수로 받는다
        return HttpResponse(content=json_data, content_type='application/json')
