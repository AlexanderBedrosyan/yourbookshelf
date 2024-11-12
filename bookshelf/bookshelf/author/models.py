from django.db import models

from bookshelf.accounts.models import CustomerModel


# Create your models here.


class Author(models.Model):
    first_name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    last_name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    date_of_birth = models.DateField(
        blank=False,
        null=False
    )
    bio = models.TextField()
    picture_url = models.URLField(
        blank=True,
        null=True
    )
    user = models.OneToOneField(
        to=CustomerModel,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"