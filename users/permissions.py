from rest_framework.permissions import BasePermission
from users.models import UserETU


class UserIsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class StudentIsLead(BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type == UserETU.UserType.LEAD:
            return True
        return False


class IsOwnerProfile(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        return False

