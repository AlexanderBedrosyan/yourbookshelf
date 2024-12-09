from django import forms
from .models import Author


class BaseAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ['user', 'approved']


class UpdateAuthorForm(BaseAuthorForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and not self.initial.get('date_of_birth'):
            self.initial['date_of_birth'] = self.instance.date_of_birth

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if not date_of_birth:
            raise forms.ValidationError("Date of birth is required.")
        return date_of_birth


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