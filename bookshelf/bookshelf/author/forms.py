from django import forms
from .models import Author


class BaseAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ['user',]


class UpdateAuthorForm(BaseAuthorForm):
    pass