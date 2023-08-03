from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.utils import create_instance, delete_instance

from .models import User, UserFollow
from .serializers import UserFollowSerializer, UserSerializer


class CustomUserViewSet(UserViewSet):
    """Кастомный viewset для эндпоинта 'users/'"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    http_method_names = ['get', 'post', 'delete']

    # Action-метод для получения объектов подписок.
    @action(methods=['get'], detail=False, url_path='subscriptions',
            permission_classes=[IsAuthenticated])
    def get_subscriptions(self, request):
        """Action-метод для получения списка подписок."""

        queryset = [
            user.author for user in UserFollow.objects.filter(
                user=request.user
            )
        ]
        context = self.get_serializer_context()
        # Проверка на необходимость пагинации респонса.
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserFollowSerializer(
                page, many=True, context=context
            )
            return self.get_paginated_response(serializer.data)
        serializer = UserFollowSerializer(
            data=queryset, context=context, many=True
        )
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Взаимодействие с отдельными объектами пользователей реализовано через
    # кастомные функции создания-удаления в action-методах.
    @action(methods=['post'], detail=True, url_path='subscribe',
            permission_classes=[IsAuthenticated])
    def user_follow(self, request, id=None):
        """Action-метод для создания объекта подписки."""

        model = UserFollow
        serializer = UserFollowSerializer
        context = self.get_serializer_context()
        message = {"error": "Вы уже подписаны на этого пользователя."}
        instance = 'author'
        objects = {
            'user': self.request.user,
            'author': self.get_object()
        }

        return create_instance(
            model, serializer, context, message, instance, objects
        )

    @user_follow.mapping.delete
    def delete_user_follow(self, request, id=None):
        """Action-метод для удаления объекта подписки."""

        model = UserFollow
        message = {"error": "Нет подписки на пользователя."}
        objects = {
            'user': self.request.user,
            'author': self.get_object()
        }

        return delete_instance(model, message, objects)
