from django import forms
from apps.news.models import News
from apps.forms import FormMixin

class WriteNewsForm(forms.ModelForm,FormMixin):
    category = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category','author','pub_time']