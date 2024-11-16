from django import forms
from .models import Author


class BaseAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ['user', 'approved']


class UpdateAuthorForm(BaseAuthorForm):
    pass


class CreateAuthorForm(BaseAuthorForm):
    class Meta(BaseAuthorForm.Meta):
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name...'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name...'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short Bio...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address...'}),
            'picture_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image url...'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }
        labels = {
            'date_of_birth': 'Date of Birth'
        }