from django.contrib import admin

# Register your models here.
from status.forms import StatusForm
from status.models import Status


class StatusAdmin(admin.ModelAdmin):
    list_display = ['user', '__str__', 'image']
    # form을 등록함으로써 admin에서 데이터를 입력할 때 validation을 추가할 수 있다.
    form = StatusForm

    # class Meta:
    #     model = Status


admin.site.register(Status, StatusAdmin)

