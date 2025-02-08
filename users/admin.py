from django.contrib import admin
from .models import User, Profile

# Register the User model with the admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id',)
    ordering = ('email',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'profile_picture', 'country')
    search_fields = ('user__email', 'first_name', 'last_name')
    readonly_fields = ('id',)
    ordering = ('user__email',)
