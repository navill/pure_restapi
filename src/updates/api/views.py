import json

from django.http import HttpResponse

from config.mixin import HttpResponseMixin
from updates.api.mixins import CSRFExemptMixin
from updates.api.utils import is_json
from updates.forms import UpdateModelForm
from updates.models import Update as UpdateModel
from django.views.generic import View


# retrieve, create, update, delete
class UpdateModelDetailAPIView(HttpResponseMixin, CSRFExemptMixin, View):
    """
    Retrieve, update, delete -> single object
    """
    is_json = True

    def get_object(self, id=None):
        # try:
        #     obj = UpdateModel.objects.get(id=id)
        # except UpdateModel.DoesNotExist:
        #     obj = None
        """
        below handles a Does Not exist exception too
        """
        qs = UpdateModel.objects.filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get(self, request, id, *args, **kwargs):
        # print(request.GET.get('id'))
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({'message': 'Update not found'})
            return self.render_to_response(error_data, status=404)
        json_data = obj.serialize()
        return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        data = json.dumps({'message': 'Not allowed, please use the /api/updates/ endpoint'})
        return self.render_to_response(data, status=403)

    def put(self, request, id, *args, **kwargs):
        # json validation
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent, please send using JSON.'})
            return self.render_to_response(error_data, status=400)
        # get object
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({'message': 'Update not found'})
            return self.render_to_response(error_data, status=404)

        # parser
        saved_data = json.loads(obj.serialize())
        pass_data = json.loads(request.body)
        # saved_data = {
        #     'user': obj.user,
        #     'text': obj.text
        # }
        for key, value in pass_data.items():
            saved_data[key] = value

        # forming
        form = UpdateModelForm(saved_data, instance=obj)
        # form valid
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = json.dumps(saved_data)  # 또는 obj.serialize()
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            # text가 비었을 경우 아래와 같은 결과 출력
            # output: {"__all__": ["Content or image is required"]}
            return self.render_to_response(data, status=400)

        json_data = json.dumps({'message': 'something'})
        return self.render_to_response(json_data)

    def delete(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({'message': 'Update not found'})
            return self.render_to_response(error_data, status=404)
        deleted, item_deleted = obj.delete()
        print(deleted, item_deleted)
        # print(deleted)
        if deleted == 1:
            json_data = json.dumps({'message': 'Successfully deleted object'})
            return self.render_to_response(json_data, status=200)
        # 비정상적인 삭제
        error_data = json.dumps({'message': 'Could not delete item.'})
        return self.render_to_response(error_data, status=403)


# Like ViewSets - one endpoint for CRUDL
# GET: api/updates/ -> List
# Post: api/updates/ -> Create
# GET: api/updates/1 -> Retrieve
# PUT: api/updates/1 -> Update
# DELETE: api/updates/1 -> Delete
class UpdateModelListAPIView(HttpResponseMixin, CSRFExemptMixin, View):
    """
    List  -> retrieve(detail)
    create
    udpate
    delete
    """
    is_json = True
    queryset = None

    def get_queryset(self):
        qs = UpdateModel.objects.all()
        self.queryset = qs
        return qs

    def get_object(self, id=None):
        if id is None:
            return None
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def render_to_response(self, data, status=200):
        return HttpResponse(data, content_type='application/json', status=status)

    def get(self, request, *args, **kwargs):
        data = json.loads(request.body)
        passed_id = data.get('id', None)
        if passed_id is not None:
            obj = self.get_object(id=passed_id)
            if obj is None:
                error_data = json.dumps({'messeage': 'object not found'})
                return self.render_to_response(error_data, status=404)
            json_data = obj.serialize()
            return self.render_to_response(json_data)
        else:
            qs = self.get_queryset()
            json_data = qs.serialize()
            return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        # json validation
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent, please send using JSON.'})
            return self.render_to_response(error_data, status=400)
        data = json.loads(request.body)
        form = UpdateModelForm(data)
        print(form)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = obj.serialize()
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            # text가 비었을 경우 아래와 같은 결과 출력
            # output: {"__all__": ["Content or image is required"]}
            return self.render_to_response(data, status=400)
        data = {'message': 'Not Allowed'}
        return self.render_to_response(data, status=400)

    # def delete(self, request, *args, **kwargs):
    #     data = json.dumps({'meesage': 'Not allowed'})
    #     # return HttpResponse(data, content_type='application/json', status=status_code)  # json
    #     return self.render_to_response(data, status=403)

    def put(self, request, *args, **kwargs):
        # json validation
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent, please send using JSON.'})
            return self.render_to_response(error_data, status=400)
        pass_data = json.loads(request.body)
        pass_id = pass_data.get('id')
        if not pass_id:
            error_data = json.dumps({'id': 'This is a required field to update an item.'})
            return self.render_to_response(error_data, status=400)
        # get object
        obj = self.get_object(id=pass_id)
        if obj is None:
            error_data = json.dumps({'message': 'Object not found'})
            return self.render_to_response(error_data, status=404)

        # parser
        saved_data = json.loads(obj.serialize())

        for key, value in pass_data.items():
            saved_data[key] = value

        # forming
        form = UpdateModelForm(saved_data, instance=obj)
        # form valid
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = json.dumps(saved_data)  # 또는 obj.serialize()
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            # text가 비었을 경우 아래와 같은 결과 출력
            # output: {"__all__": ["Content or image is required"]}
            return self.render_to_response(data, status=400)

        json_data = json.dumps({'message': 'something'})
        return self.render_to_response(json_data)

    def delete(self, request, *args, **kwargs):
        # json validation
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent, please send using JSON.'})
            return self.render_to_response(error_data, status=400)
        pass_data = json.loads(request.body)
        pass_id = pass_data.get('id')
        if not pass_id:
            error_data = json.dumps({'id': 'This is a required field to update an item.'})
            return self.render_to_response(error_data, status=400)

        # get object
        obj = self.get_object(id=pass_id)
        if obj is None:
            error_data = json.dumps({'message': 'Object not found'})
            return self.render_to_response(error_data, status=404)

        deleted, item_deleted = obj.delete()
        print(deleted, item_deleted)
        # print(deleted)
        if deleted == 1:
            json_data = json.dumps({'message': 'Successfully deleted object'})
            return self.render_to_response(json_data, status=200)
        # 비정상적인 삭제 실패
        error_data = json.dumps({'message': 'Could not delete item.'})
        return self.render_to_response(error_data, status=403)
