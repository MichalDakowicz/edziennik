from rest_framework import permissions
from decouple import config


class IsAdminKeyAuthenticated(permissions.BasePermission):
    """
    Allows access only if the 'ADMIN-KEY' header matches the one in settings.
    """

    def has_permission(self, request, view):
        expected_key = config("ADMIN-KEY", default=None)
        if not expected_key:
            # If server is not configured with an ADMIN-KEY, decide whether to allow or block.
            # Assuming block for security.
            return False

        received_key = request.headers.get("ADMIN-KEY")
        return received_key == expected_key
