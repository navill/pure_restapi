import json

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.reverse import reverse as api_reverse
from accounts.api.serializers import UserPublicSerializer
from status.models import Status, QuadModel

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


class StatusInlineUserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Status
        fields = [
            'url', 'id', 'content', 'image'
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        return api_reverse('api_status:detail', kwargs={"id": obj.id}, request=request)


class CustomSerializer(serializers.Serializer):
    content = serializers.CharField()
    email = serializers.EmailField()


class StatusSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    user = UserPublicSerializer(read_only=True)

    # user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    # user_hyperlink = serializers.HyperlinkedRelatedField(source='user', lookup_field='username',
    #                                                      view_name='api_user:detail', read_only=True)
    # username = serializers.SlugRelatedField(read_only=True, source='user', slug_field='username')

    class Meta:
        model = Status
        fields = [
            'url', 'id',
            # 'user_id', 'user_hyperlink', 'username',
            'user', 'content', 'image'
        ]
        read_only_fields = ['user']  # GET

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

    def get_url(self, obj):
        request = self.context.get('request')
        return api_reverse('status:detail', kwargs={"id": obj.id}, request=request)


class QuadSerializer(serializers.ModelSerializer):
    choice_field = serializers.SerializerMethodField()

    class Meta:
        model = QuadModel
        fields = ['choice_field', 'chr']

    #
    # def __init__(self, *args, **kwargs):
    #     super(LectureAdminForm, self).__init__(*args, **kwargs)
    #     obj = kwargs.get('instance')  # Lecture
    #     # lecture에서 video를 가지고 있지 않은(null) Video 객체를 filtering
    #     qs = Video.objects.unused()
    #     if obj:
    #         if obj.video:
    #             this_ = Video.objects.filter(pk=obj.video.pk)
    #             qs = (qs | this_)
    #         self.fields['video'].queryset = qs
    #     else:
    #         self.fields['video'].queryset = qs

    def get_choice_field(self, obj):
        if not obj.choice_field:
            return None
        # print(obj.get_choice_field_display())
        return obj.choice_field
