from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from recipes.views import RecipeViewSet, TagViewSet, UserViewSet


router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'users', UserViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
