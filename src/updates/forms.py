from django import forms

from updates.models import Update as UpdateModel


class UpdateModelForm(forms.ModelForm):
    class Meta:
        model = UpdateModel
        fields = ['user', 'text', 'image']
