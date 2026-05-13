from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class UserOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method =='PATCH':
            return bool(request.user and (request.user.is_superuser or request.user == obj.user))
        elif request.method =='DELETE':
            return bool(request.user and request.user.is_superuser)

class IsBusinessUserOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return bool(request.user and (request.user.is_superuser or request.user.profile.type == 'business'))