from django.contrib import admin
from bookshelf.author.models import Author

# Register your models here.


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'date_of_birth', 'approved', 'user', 'picture_available')
    search_fields = ('first_name', 'last_name', 'bio', 'user__username')
    list_filter = ('approved', 'date_of_birth')
    fields = ('first_name', 'last_name', 'date_of_birth', 'bio', 'picture_url', 'user', 'approved')
    actions = ['approve_authors', 'revoke_approval']
    readonly_fields = ('full_name',)

    def full_name(self, obj):
        return obj.get_full_name()

    full_name.short_description = "Full Name"

    def approve_authors(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Selected authors have been approved.")

    approve_authors.short_description = "Approve selected authors"

    def revoke_approval(self, request, queryset):
        queryset.update(approved=False)
        self.message_user(request, "Approval revoked for selected authors.")

    revoke_approval.short_description = "Revoke approval for selected authors"

    def picture_available(self, obj):
        return bool(obj.picture_url)

    picture_available.short_description = "Picture Available"
    picture_available.boolean = True
