from rest_framework import permissions


#
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Стандартный пермишен для взаимодействия с отдельными
    элементами моделей.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
