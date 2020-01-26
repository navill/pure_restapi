from django.contrib.auth import get_user_model
from rest_framework import serializers

# from status.api.serializers import StatusInlineUserSerializer
from status.api.serializers import StatusInlineUserSerializer
from rest_framework.reverse import reverse as api_reverse

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    # statuses = serializers.HyperlinkedRelatedField(source='status_set',  # Status.objects.filter(user=user)
    #                                                many=True, read_only=True, lookup_field='id',
    #                                                view_name='api_status:detail')

    # status_url = serializers.SerializerMethodField(read_only=True)
    # recent_status = serializers.SerializerMethodField(read_only=True)

    statuses = StatusInlineUserSerializer(source='status_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'statuses', 'url', 'status',
        ]

    def get_status(self, obj):
        request = self.context.get('request')
        limit = 10
        if request:
            limit_query = request.GET.get('limit')
            try:
                limit = int(limit_query)
            except:
                pass
        qs = obj.status_set.all().order_by('-timestamp')  # Status.objects.filter(user=obj)
        data = {
            'url': self.get_url(obj) + 'status/',
            'last': StatusInlineUserSerializer(qs.first()).data,
            'recent': StatusInlineUserSerializer(qs[:limit], many=True).data
        }
        return data

    def get_url(self, obj):
        request = self.context.get('request')
        return api_reverse("api_user:detail", kwargs={"username": obj.username}, request=request)
