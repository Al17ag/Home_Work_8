from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """ Пермишен, который позволяет изменять или удалять объект только его владельцу."""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user    # Проверяем, является ли текущий пользователь владельцем объекта