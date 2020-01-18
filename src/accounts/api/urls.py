from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from accounts.api.views import AuthAPIView, RegisterAPIView

app_name = 'accounts'

urlpatterns = [
    path('jwt/', obtain_jwt_token),
    path('jwt/refresh/', refresh_jwt_token),
    path('register/', RegisterAPIView.as_view()),
    path('', AuthAPIView.as_view()),
]
