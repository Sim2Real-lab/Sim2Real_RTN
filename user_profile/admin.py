from django.contrib import admin
from .models import UserProfile
# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'contact', 'branch', 'college', 'year', 'dob','event_year')
    search_fields = ('user__username', 'first_name', 'last_name', 'college')
    list_filter = ('branch', 'college', 'year')

    fieldsets = (
        (None, {'fields': ('user', 'first_name', 'last_name', 'contact', 'branch', 'college', 'year', 'dob', 'photo','event_year')}),
    )
