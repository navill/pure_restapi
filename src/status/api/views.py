import json

from django.views.generic import ListView
from django.views.generic.base import View
from rest_framework import generics, mixins, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView

from accounts.api.permissions import IsOwnerOrReadOnly
from status.models import Status
from .serializers import StatusSerializer


def is_json(json_data):
    try:
        real_json = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid


class StatusDetailAPIView(mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # authentication_classes = []
    serializer_class = StatusSerializer
    queryset = Status.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    # def perform_update(self, serializer):
    #     serializer.save(updated_by_user=self.request.user)
    #
    # def perform_destroy(self, instance):
    #     if instance is not None:
    #         return instance.delete()
    #     return None


class StatusAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView):  # Create + List
    # login required mixin
    # permission -> 객체에 어떤 권한을 줄것인가?
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # authentication -> 인증을 어떻게 할 것인가?
    # authentication_classes = [SessionAuthentication]  # Oauth, JWT

    serializer_class = StatusSerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = Status.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # serializer를 통해 객체 생성 중 user에 request.user를 입력한다.
    def perform_create(self, serializer):  # perform_create -> 새 객체 생성 시 CreateModelMixin 호출
        serializer.save(user=self.request.user)

# class StatusAPIView(
#     mixins.CreateModelMixin,
#     generics.ListAPIView):  # Create + List
#
#     permission_classes = []
#     authentication_classes = []
#
#     serializer_class = StatusSerializer
#     passed_id = None
#
#     def make_passed_id(self, request):
#         # url에 id를 포함하여 요청이 들어올 경우
#         url_passed_id = request.GET.get('id', None)
#         # data에 id를 포함하여 요청이 들어올 경우 처리
#         json_data = {}
#         body_ = request.body
#
#         if is_json(body_):
#             # 유효성 검사를 하지 않고 json.loads(request.body)를 사용할 경우 Json decode 에러 발생
#             json_data = json.loads(request.body)
#         new_passed_id = json_data.get('id', None)
#         passed_id = url_passed_id or new_passed_id or None
#
#         self.passed_id = passed_id
#         return passed_id
#
#     def get_queryset(self):
#         request = self.request
#         qs = Status.objects.all()
#         query = request.GET.get('q')
#         if query is not None:
#             qs = qs.filter(content__icontains=query)
#         return qs
#
#     def get_object(self):
#         request = self.request
#         # request.body를 통해 들어오는 id값을 확인하기 위해 self.passed_id 추가
#         passed_id = request.GET.get('id', None) or self.passed_id
#         qs = self.get_queryset()
#         obj = None
#         if passed_id is not None:
#             obj = get_object_or_404(qs, id=passed_id)
#             self.check_object_permissions(request, obj)
#         return obj
#
#     def get(self, request, *args, **kwargs):
#         passed_id = self.make_passed_id(request)
#         if passed_id is not None:
#             # id from url + id from request.data
#             return self.retrieve(request, *args, **kwargs)  # -> get_object 호출
#         return super(StatusAPIView, self).get(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class StatusDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer


# class StatusDetailAPIView(mixins.DestroyModelMixin, mixins.UpdateModelMixin,
#                           generics.RetrieveAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#
#     # # url에 pk대신 다른 변수명을 사용할 경우 lookup_field나 get_object를 이용해 처리
#     # lookup_field = 'id'
#     #
#     # def get_object(self):
#     #     kwargs = self.kwargs
#     #     kw_id = kwargs.get('id')
#     #     return Status.objects.get(id=kw_id)
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

#
# class StatusUpdateAPIView(generics.UpdateAPIView):
#     permission_classes = []
#     authentication_classes = []
#
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#
#
# class StatusDeleteAPIView(generics.DestroyAPIView):
#     permission_classes = []
#     authentication_classes = []
#
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer

