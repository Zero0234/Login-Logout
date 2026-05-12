from django.contrib import admin
from .models import NetlabLog

@admin.register(NetlabLog)
class NetlabLogAdmin(admin.ModelAdmin):
    # Columns shown in the admin table
    list_display = ('name', 'role', 'id_number', 'timestamp')
    
    # Right sidebar filters
    list_filter = ('role', 'timestamp')
    
    # Search bar configuration
    search_fields = ('name', 'id_number')
    
    # Protect the timestamp from manual edits
    readonly_fields = ('timestamp',)
    
    list_per_page = 50