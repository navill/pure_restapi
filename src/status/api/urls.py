from django.contrib import admin
from django.urls import path, include

from status.api.views import StatusAPIView, StatusDetailAPIView

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

# app_name = 'api_status'

urlpatterns = [
    path('', StatusAPIView.as_view()),
    path('<id>/', StatusDetailAPIView.as_view(), name='detail'),
]
