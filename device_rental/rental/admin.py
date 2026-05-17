from django.contrib import admin
from .models import Device, RentalRecord

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    # 在列表頁一眼看出狀態
    list_display = ['section', 'device_type', 'name', 'is_bulk', 'is_active']
    # 支援右側快速過濾
    list_filter = ['section', 'device_type', 'is_active', 'is_bulk']
    # 搜尋功能 (管理員可以直接搜名稱修改)
    search_fields = ['name']

@admin.register(RentalRecord)
class RentalRecordAdmin(admin.ModelAdmin):
    list_display = ['date', 'period', 'school_section', 'student_name', 'student_class', 'device', 'quantity']
    list_filter = ['date', 'period', 'school_section']


# Register your models here.
