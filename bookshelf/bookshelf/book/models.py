from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models import Avg
from bookshelf.accounts.models import CustomerModel
from bookshelf.author.models import Author
from .validators import UpperValueValidator
from .choices import GenreChoices, BookStatusChoices


# Create your models here.

class Book(models.Model):
    user = models.ForeignKey(
        to=CustomerModel,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        to=Author,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='books'
    )
    picture_url = models.URLField(
        blank=False,
        null=False
    )
    description = models.TextField(
        validators=[MaxLengthValidator(2000), UpperValueValidator()],
        help_text="Not more than 2000 characters and first letter should be upper or in Book an allowed quotation symbol."
    )
    title = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        unique=True
    )
    approved = models.BooleanField(
        default=False
    )
    genre = models.CharField(
        max_length=40,
        choices=GenreChoices.choices,
        default=GenreChoices.OTHERS
    )

    def __str__(self):
        return self.title

    def average_rating(self):
        return self.ratings.aggregate(Avg('rating'))['rating__avg'] or 0


class Comment(models.Model):
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        to=CustomerModel,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {str(self.book)}"


class Rating(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    user = models.ForeignKey(
        to=CustomerModel,
        on_delete=models.CASCADE
    )
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    class Meta:
        unique_together = ('book', 'user')


class UserBookStatus(models.Model):
    user = models.ForeignKey(to=CustomerModel, on_delete=models.CASCADE, related_name="book_statuses")
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="user_statuses")
    status = models.CharField(
        max_length=50,
        choices=BookStatusChoices.choices,
        default=BookStatusChoices.NONE
    )

    class Meta:
        unique_together = ('user', 'book')