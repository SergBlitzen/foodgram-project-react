from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from recipes.views import RecipeViewSet, TagViewSet, IngredientViewSet
from users.views import CustomUserViewSet

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
]
