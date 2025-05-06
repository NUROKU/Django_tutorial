from django.contrib import admin
from .models import User, UserActivateTokens
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
admin.site.register(User)
admin.site.register(UserActivateTokens)