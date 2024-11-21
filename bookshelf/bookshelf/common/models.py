from django.db import models

from bookshelf.accounts.models import CustomerModel


# Create your models here.


class Report(models.Model):
    title = models.CharField(
        max_length=100
    )
    user = models.ForeignKey(
        to=CustomerModel,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    report_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title