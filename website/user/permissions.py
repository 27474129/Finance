from rest_framework.permissions import BasePermission

from user.services import Auth


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return True if Auth().decode_token(request.session.get('token')) \
            else False
