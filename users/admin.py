from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import CustomUser, Profile

@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'telegram_username', 'is_agent', 'create_date', 'last_update')
    list_filter = ('is_agent',)
    search_fields = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'telegram_username')
    date_hierarchy = 'create_date'

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'phone_number', 'email', 'is_agent', 'telegram_username', 'x_link', 'm_link', 'l_link', 'profile_image', 'create_date', 'last_update')
    list_filter = ('is_agent',)
    search_fields = ('user__username', 'user__email', 'phone_number', 'first_name', 'last_name', 'telegram_username')
    date_hierarchy = 'create_date'
