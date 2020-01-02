from django.urls import path

from updates.api.views import UpdateModelListAPIView, UpdateModelDetailAPIView


app_name = 'api'

urlpatterns = [
    path('', UpdateModelListAPIView.as_view()),  # list & create
    # path('json/serialized/list/', SerializerListView.as_view()),
    path('<int:id>', UpdateModelDetailAPIView.as_view()),
]
