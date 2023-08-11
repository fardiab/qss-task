from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'surname', 'username', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('email', 'name', 'surname', 'username', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'name', 'surname', 'username', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    readonly_fields = ('date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
