from django.contrib import admin
from django.urls import path, include

from status.api.views import StatusListSearchAPIView, StatusAPIView, StatusCreateAPIView, StatusDetailAPIView, \
    StatusUpdateAPIView, StatusDeleteAPIView

app_name = 'status'

"""
/api/status/ -> list
/api/status/create -> create
/api/status/12/ -> detail
/api/status/12/update/ -> update
/api/status/12/delete/ -> delete


/api/status/ -> List -> CRUDL
/api/status/12/ -> Detail -> CRUDL

/api/status/ -> CRUDL + search
"""

urlpatterns = [
    path('', StatusAPIView.as_view()),
    path('create/', StatusCreateAPIView.as_view()),
    path('<pk>/', StatusDetailAPIView.as_view()),
    path('<pk>/update/', StatusUpdateAPIView.as_view()),
    path('<pk>/delete/', StatusDeleteAPIView.as_view()),
]
