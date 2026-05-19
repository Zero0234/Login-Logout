from django.contrib import admin
from .models import NetlabLog, LearnerProfile
from import_export.admin import ImportExportModelAdmin

# Registers the new Master List in the Admin Panel
@admin.register(LearnerProfile)
class LearnerProfileAdmin(ImportExportModelAdmin):
    list_display = ('id_number', 'full_name')
    search_fields = ('id_number', 'full_name')
    ordering = ('id_number',)

# Our existing Daily Log configuration
@admin.register(NetlabLog)
class NetlabLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'id_number', 'timestamp')
    list_filter = ('role', 'timestamp')
    search_fields = ('name', 'id_number')
    readonly_fields = ('timestamp',)
    list_per_page = 50