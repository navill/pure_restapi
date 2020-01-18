from rest_framework import serializers

from status.models import Status

"""
# forms.py
폼 형태와 거의 동일하다.
class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = [
            'user', 'content', 'image'
        ]
        
serializers -> JSON 데이터 처리 + Validation
"""


class CustomSerializer(serializers.Serializer):
    content = serializers.CharField()
    email = serializers.EmailField()


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
            'user', 'content', 'image'
        ]

    # model field level validation
    # def validate_<field_name>
    # def validate_content(self, value):
    #     if len(value) > 10000:
    #         raise serializers.ValidationError('to much')
    #     return value

    # serializer level validation
    def validate(self, data):
        content = data.get('content', None)
        if content == "":
            content = None

        image = data.get('image', None)
        if content is None and image is None:
            raise serializers.ValidationError('Content or image is required.')
        return data