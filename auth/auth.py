from rest_framework.permissions import IsAuthenticated


class IsSuperUser(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsPengurus(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_pengurus()
