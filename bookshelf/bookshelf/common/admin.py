from django.contrib import admin
from bookshelf.common.models import Report


# Register your models here.

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass