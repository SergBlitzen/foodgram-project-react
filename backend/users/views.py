from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from djoser.views import UserViewSet

from .models import User, UserFollow
from .serializers import UserSerializer, UserFollowSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=False, url_path='subscriptions',
            permission_classes=[IsAuthenticated])
    def get_subscriptions(self, request):
        queryset = [user.author for user in UserFollow.objects.filter(user=request.user)]
        context = self.get_serializer_context()
        serializer = UserFollowSerializer(data=queryset, context=context, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    http_method_names = ['get', 'post']
