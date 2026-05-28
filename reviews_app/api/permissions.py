from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class IsCustomerUserOrAdmin(BasePermission):
    """
    Custom permission to only allow board Superuser and User.

    Users are granted access if they are either:
    - Superuser =   POST
    - Customer User    =   POST
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return bool(request.user and (request.user.is_superuser or request.user.profile.type == 'customer'))
        return True

class UserOrAdmin(BasePermission):
    """
    Custom permission to only allow board Superuser and User.

    Users are granted access if they are either:
    - Superuser =   SAFE_METHODS, PATCH, DELETE
    - Reviewer User    =   SAFE_METHODS, PATCH
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'PATCH':
            return bool(request.user and (request.user.is_superuser or request.user == obj.reviewer))
        elif request.method == 'DELETE':
            return bool(request.user and (request.user.is_superuser or request.user == obj.reviewer))
