from django.contrib import admin
from .models import NetlabLog, LearnerProfile
from import_export.admin import ImportExportModelAdmin

# Student Master List
@admin.register(LearnerProfile)
class LearnerProfileAdmin(ImportExportModelAdmin):
    list_display = ('id_number', 'full_name', 'get_department_upper')
    search_fields = ('id_number', 'full_name')
    ordering = ('id_number',)

    def get_department_upper(self, obj):
        return str(obj.department).upper() if obj.department else "-"
    get_department_upper.short_description = 'Department'

# Daily Log
@admin.register(NetlabLog)
class NetlabLogAdmin(ImportExportModelAdmin):
    list_display = ('name', 'role', 'id_number', 'get_department_upper', 'purpose', 'timestamp')
    list_filter = ('role', 'timestamp')
    search_fields = ('name', 'id_number')
    readonly_fields = ('timestamp',)
    list_per_page = 50

    def get_department_upper(self, obj):
        return str(obj.department).upper() if obj.department else "-"
    get_department_upper.short_description = 'Department'