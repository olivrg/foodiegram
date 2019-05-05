from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrSuperUser(permissions.BasePermission):
    """do not allow user to delete anything without superuser privilege"""

    def has_permission(self, request, view):
        """check if user is superuser. if not superuser, cannot delete """
        if_superuser = request.user.is_superuser
        # user is not superuser
        if if_superuser:
            return True
        # user can't delete user entry
        else:
            if request.method == "DELETE":
                raise PermissionDenied(
                    'Sorry, you must be an admin for that action.'
                )
            # users can edit own entry
            else:
                return True


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            raise PermissionDenied(
                'Sorry, you must be an admin for that action.'
            )
