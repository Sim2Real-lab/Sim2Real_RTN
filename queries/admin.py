from django.contrib import admin

# Register your models here.

from .models import Query

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display=('ticket','contact','message','created_at','query_type','resolved','response')
    list_filter = ('query_type', 'resolved')
    search_fields = ('ticket', 'email','contact')
    readonly_fields = ('ticket','sender','email','name','contact','query_type','message','organisation','created_at')

    # This controls the order of fields in the form
    fields = (
        'ticket', 'sender', 'email', 'name', 'contact','created_at',
        'organisation', 'query_type', 'message', 'response',
        'resolved'
    )