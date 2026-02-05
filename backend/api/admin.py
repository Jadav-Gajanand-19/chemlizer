from django.contrib import admin
from .models import Equipment, UploadHistory


@admin.register(UploadHistory)
class UploadHistoryAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'num_records', 'uploaded_at']
    list_filter = ['uploaded_at', 'user']
    search_fields = ['filename']
    readonly_fields = ['uploaded_at']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'upload_session']
    list_filter = ['equipment_type', 'upload_session']
    search_fields = ['equipment_name', 'equipment_type']
