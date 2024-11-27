from django.contrib import admin
from bookshelf.accounts.models import CustomerModel
from bookshelf.common.models import QuizResults


# Register your models here.
@admin.register(CustomerModel)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'get_quiz_rating', 'get_roles')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    fields = ('username', 'email', 'first_name', 'last_name', 'picture_url', 'is_staff', 'is_active', 'groups', 'get_roles', 'get_quiz_rating', 'level')
    readonly_fields = ('username', 'get_roles', 'get_quiz_rating', 'level')
    actions = ['mark_as_staff', 'deactivate_users']

    def mark_as_staff(self, request, queryset):
        queryset.update(is_staff=True)
        self.message_user(request, "Selected users have been marked as staff.")

    mark_as_staff.short_description = "Mark selected users as staff"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected users have been deactivated.")

    deactivate_users.short_description = "Deactivate selected users"

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.fields
        return self.readonly_fields

    def get_roles(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    get_roles.short_description = "Roles"

    def get_quiz_rating(self, obj):
        quiz_obj = QuizResults.objects.get(id=obj.id)
        return quiz_obj.points

    get_quiz_rating.short_description = "Quiz Rating Points"

    def level(self, obj):
        quiz_obj = QuizResults.objects.get(id=obj.id)
        return quiz_obj.level

    level.short_description = "Level"
