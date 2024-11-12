from django.contrib import admin

from bookshelf.accounts.models import CustomerModel


# Register your models here.
@admin.register(CustomerModel)
class CustomerAdmin(admin.ModelAdmin):
    pass