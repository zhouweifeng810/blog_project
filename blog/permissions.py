# blog/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, "author_id", None) == getattr(
            getattr(request, "user", None), "id", None
        )
class IsCommentOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        u = request.user
        return (u and u.is_authenticated and (u.is_staff or obj.author_id == u.id))
