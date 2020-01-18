from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        pw = data.get('password')
        # password2는 계정 생성 시 유효하지 않 변수로 판단하여기 때문에 포함되면 안됨
        # TypeError: 'password2' is an invalid keyword argument for this function
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError('Password must match')
        return data

    def create(self, validated_data):
        print(validated_data)
        user_obj = User(username=validated_data.get('username'),
                        email=validated_data.get('email'))
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj
