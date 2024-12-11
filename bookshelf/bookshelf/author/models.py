from django.db import models
from bookshelf.accounts.models import CustomerModel
from .validators import UpperValueValidator


# Create your models here.


class Author(models.Model):
    first_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        validators=[UpperValueValidator()]
    )
    last_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        validators=[UpperValueValidator()]
    )
    date_of_birth = models.DateField(
        blank=False,
        null=False
    )
    bio = models.TextField(
        validators=[UpperValueValidator(message="Biography must start with an uppercase letter.")]
    )
    picture_url = models.URLField(
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        to=CustomerModel,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    approved = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def formatted_bio(self):
        return self.bio.replace('\n', '<br>')