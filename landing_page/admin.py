# landing_page/admin.py
from django.contrib import admin
from .models import Sponsor, Query, GeneralQuery

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'tier')
    list_filter = ('tier',)
    search_fields = ('name',)

@admin.register(Query) # For sponsor inquiries
class QueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'organisation','mobile_number', 'contact_email', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'organisation', 'contact_email', 'message')
    readonly_fields = ('submitted_at',)

@admin.register(GeneralQuery) # For general visitor inquiries
class GeneralQueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution_name', 'contact_email', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'institution_name', 'contact_email', 'message')
    readonly_fields = ('submitted_at',)
