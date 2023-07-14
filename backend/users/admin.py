from django.contrib import admin

from .models import User, UserFollow


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')


class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(UserFollow, UserFollowAdmin)