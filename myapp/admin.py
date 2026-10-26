from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
# Register your models here.
class CustomUserAdmin(UserAdmin):
  model = UserProfile
  list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
  fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('role',)}),)
  add_fieldsets = UserAdmin.add_fieldsets + (
      (None, {'fields': ('email', 'role')}),
  )


admin.site.register(UserProfile, CustomUserAdmin)