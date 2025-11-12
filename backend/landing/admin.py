from django.contrib import admin
from .models import MobileRecord


@admin.register(MobileRecord)
class MobileRecordAdmin(admin.ModelAdmin):
    """
    Admin interface for MobileRecord model.
    """
    list_display = ['mobile', 'created_at']
    list_filter = ['created_at']
    search_fields = ['mobile']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    date_hierarchy = 'created_at'