from django import forms

from bookshelf.author.models import Author
from bookshelf.book.models import Book, Comment


class BaseBookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['approved', 'user']


class BaseCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class UpdateCommentForm(BaseCommentForm):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control'}
        ),
        required=True
    )


class DeleteCommentForm(BaseBookForm):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control'}
        ),
        required=True
    )


class CreateBookForm(BaseBookForm):
    author = forms.CharField(
        label="Author",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter author’s full name (first and last name)'
        }),
        error_messages={
            'required': "You must provide the author's full name."
        }
    )

    class Meta(BaseBookForm.Meta):
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title...'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description...'}),
            'picture_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image url...'}),
        }

    def clean_author(self):
        author_name = self.cleaned_data.get('author')
        try:
            first_name, last_name = author_name.split(' ', 1)
            author = Author.objects.get(first_name=first_name, last_name=last_name)
        except (ValueError, Author.DoesNotExist):
            raise forms.ValidationError("The author's name must match exactly as it is in the YourBookShelf app.")
        return author

    def save(self, commit=True):
        book = super().save(commit=False)
        book.author = self.cleaned_data['author']
        if commit:
            book.save()
        return book

