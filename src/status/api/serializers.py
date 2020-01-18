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


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
            'user', 'content', 'image'
        ]
