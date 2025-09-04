from django.contrib import admin
from .models import Announcments  # Consider renaming this to 'Announcement' for clarity

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['message', 'category', 'valid_till', 'created_at', 'created_by']
    list_filter = ['category', 'valid_till']
    search_fields = ['message', 'created_by__username']

admin.site.register(Announcments, AnnouncementAdmin)
