from django import forms

from bookshelf.book.models import Book, Comment


class BaseBookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['approved']


class CreateBookForm(BaseBookForm):
    pass


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