from django.contrib import admin
from bookshelf.common.models import Report, QuizResults


# Register your models here.

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass


@admin.register(QuizResults)
class ReportAdmin(admin.ModelAdmin):
    pass