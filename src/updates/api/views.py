from django.http import HttpResponse

from updates.models import Update as UpdateModel
from django.views.generic import View


# retrieve, create, update, delete
class UpdateModelDetailAPIView(View):
    """
    Retrieve, update, delete -> single object
    """

    def get(self, request, id, *args, **kwargs):
        # print(request.GET.get('id'))
        obj = UpdateModel.objects.get(id=id)
        json_data = obj.serialize()
        return HttpResponse(json_data, content_type='application/json')  # json

    def post(self, request, *args, **kwargs):
        return HttpResponse({}, content_type='application/json')  # json

    def put(self, request, *args, **kwargs):
        return HttpResponse({}, content_type='application/json')  # json

    def delete(self, request, *args, **kwargs):
        return HttpResponse({}, content_type='application/json')  # json


class UpdateModelListAPIView(View):
    """
    List, create
    """

    def get(self, request, *args, **kwargs):
        qs = UpdateModel.objects.all()
        json_data = qs.serialize()
        return HttpResponse(json_data, content_type='application/json')  # json

    def post(self, request, *args, **kwargs):
        return HttpResponse({}, content_type='application/json')  # json
