from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


class AuthAPIView(APIView):
    # authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # header에 token을 가지고 로그인을 시도할 경우
        if request.user.is_authenticated:
            return Response({'detail': 'You are already authenticated'}, status=400)
        data = request.data
        username = data.get('username')
        password = data.get('password')
        # user = authenticate(username=username, password=password)

        # email or username으로 인증 처리
        qs = User.objects.filter(Q(username__iexact=username) |
                                 Q(email__iexact=username)).distinct()

        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj

                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request=request)

                return Response(response)
        return Response({'detail': 'Invalid credentials'}, status=401)


class RegisterAPIView(APIView):
    # authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # header에 token을 가지고 로그인을 시도할 경우
        if request.user.is_authenticated:
            return Response({'detail': 'You are already registered and authenticated'}, status=400)
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password')

        # email or username으로 인증 처리
        qs = User.objects.filter(Q(username__iexact=username) |
                                 Q(email__iexact=username)).distinct()
        # password validation
        if password != password2:
            return Response({'password': 'Password must match.'}, status=401)
        # user validation
        if qs.exists():
            return Response({'detail': 'This user already exists'}, status=401)
        else:
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            # 로그인 완료 후 jwt payload - 전달할 필요 없음
            # payload = jwt_payload_handler(user)
            # token = jwt_encode_handler(payload)
            # response = jwt_response_payload_handler(token, user, request=request)

            return Response({'detail': 'Thank you for registering. Please verify your email'}, status=201)
        # return Response({'detail': 'Invalid credentials'}, status=401)
