from django.contrib import admin
from bookshelf.common.models import Report

# Register your models here.


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'short_report_text', 'is_recent')
    search_fields = ('title', 'user__username', 'report_text')
    list_filter = ('created_at',)
    fields = ('title', 'user', 'report_text', 'created_at', 'short_report_text')
    readonly_fields = ('created_at', 'short_report_text')
    actions = ['mark_reports_as_reviewed']

    def short_report_text(self, obj):
        return obj.report_text[:50] + "..." if len(obj.report_text) > 50 else obj.report_text
    short_report_text.short_description = "Report Summary"

    def is_recent(self, obj):
        from datetime import timedelta
        from django.utils.timezone import now
        return obj.created_at >= now() - timedelta(days=7)
    is_recent.boolean = True
    is_recent.short_description = "Created Recently"

    def mark_reports_as_reviewed(self, request, queryset):
        updated_count = queryset.update(report_text="[Reviewed] " + queryset.first().report_text)
        self.message_user(request, f"{updated_count} report(s) marked as reviewed.")
    mark_reports_as_reviewed.short_description = "Mark selected reports as reviewed"

