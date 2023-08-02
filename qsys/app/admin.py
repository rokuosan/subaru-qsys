from django.contrib import admin

from .models.app_user import AppUser

# Register your models here.
admin.site.register(AppUser)
