## Mixin

- **JsonResponseMixin**: JsonResponse(<python data:dict>, **kwargs)에 의한 데이터 직렬화

- **HttpResponseMixin:** HttpResponse(<serialized_data:json>, **kwargs)에 의한 응답

  - serialize(): HttpRespnose의 매개변수 들어갈 직렬화 데이터 생성

- **CSRFExemptMixin:** CSRF validation 무시용 mixin

  ```python
    from django.http import JsonResponse
    
    
    class JsonResponseMixin(object):
        def render_to_json_response(self, context, **response_kwargs):
            return JsonResponse(self.get_data(context), **response_kwargs)
    
        def get_data(self, context):
            return context
    
    
    class HttpResponseMixin(object):
        is_json = False
        def render_to_response(self, data, status=200):
            content_type = 'text/html'
            if self.is_json:
                content_type = 'application/json'
            return HttpResponse(data, content_type=content_type, status=status)
    
    # 유저 인증을 넘기기 위해 사용 - 테스트용
    class CSRFExemptMixin(object):
        @method_decorator(csrf_exempt)
        def dispatch(self, *args, **kwargs):
            # super(CSRFExemptMixin, self)
            return super().dispatch(*args, **kwargs)
  ```





## View

### View - UpdateModelListAPIView(CRUDL)

- Client의 HTTP method에 따른 CRUDL 동작

- 기본 메소드

  - get_queryset(): 요청된 queryset 제공

  - get_object(): 요청된 특정 객체(id) 제공

  - render_to_response(): 응답을 위해 content-type과 status 제공

    ```python
      # GET: api/updates/ -> List
      # Post: api/updates/ -> Create
      # GET: api/updates/1 -> Retrieve
      # PUT: api/updates/1 -> Update
      # DELETE: api/updates/1 -> Destroy
      
      class UpdateModelListAPIView(HttpResponseMixin, CSRFExemptMixin, View):
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
    ```

- GET(List & Retrieve)

  ```python
    def get(self, request, *args, **kwargs):
        data = json.loads(request.body)
        passed_id = data.get('id', None)
        # retrieve: id가 있을 경우
        if passed_id is not None:
            obj = self.get_object(id=passed_id)
            if obj is None:
                error_data = json.dumps({'message': 'Object not found'})
                return self.render_to_response(error_data, status=404)
            json_data = obj.serialize()
            return self.render_to_response(json_data)
        # list: id가 없을 경우
        else:
            qs = self.get_queryset()
            json_data = qs.serialize()
            return self.render_to_response(json_data)
  ```

- POST(Create)

  ```python
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
  ```

- PUT(Update)

  ```python
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
    		# ----데이터가 업데이트되는 시점----
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
    				# error message는 UpdateModelForm에 저장됨
            # output: {"__all__": ["Content or image is required"]}
            return self.render_to_response(data, status=400)
    
        json_data = json.dumps({'message': 'something'})
        return self.render_to_response(json_data)
  ```

- DELETE(Destroy)

  ```python
    def delete(self, request, *args, **kwargs):
        # json validation
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent, please send using JSON.'})
            return self.render_to_response(error_data, status=400)
        pass_data = json.loads(request.body)
        pass_id = pass_data.get('id')
    
    		# id 유무 확인
        if not pass_id:
            error_data = json.dumps({'id': 'This is a required field to update an item.'})
            return self.render_to_response(error_data, status=400)
    
        # 해당 id의 객체 유무 확인
        obj = self.get_object(id=pass_id)
        if obj is None:
            error_data = json.dumps({'message': 'Object not found'})
            return self.render_to_response(error_data, status=404)
    
        deleted, item_deleted = obj.delete()
        print(deleted, item_deleted)
    
    		# 객체 삭제 성공 여부 확인
        if deleted == 1:
            json_data = json.dumps({'message': 'Successfully deleted object'})
            return self.render_to_response(json_data, status=200)
        # 삭제 실패
        error_data = json.dumps({'message': 'Could not delete item.'})
        return self.render_to_response(error_data, status=403)
  ```

