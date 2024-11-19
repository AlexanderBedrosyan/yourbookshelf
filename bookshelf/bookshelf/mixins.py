from django.shortcuts import redirect
from django.contrib import messages


class PermissionCheckMixin:
    DENIED_MESSAGE = "Access denied. You do not have the required permissions to view this page."

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (obj.user == request.user or request.user.is_superuser or request.user.is_staff):
            messages.error(request, self.DENIED_MESSAGE)
            return redirect('permission-denied')
        return super().get(request, *args, **kwargs)