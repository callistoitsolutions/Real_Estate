from django.contrib import admin
from .models import Vendor, VendorDocument

class VendorDocumentInline(admin.TabularInline):
    model = VendorDocument
    extra = 0

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'primary_service', 'city', 'phone', 'vendor_status', 'created_at')
    search_fields = ('business_name', 'contact_person', 'city', 'special_tags')
    inlines = [VendorDocumentInline]

@admin.register(VendorDocument)
class VendorDocumentAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'file', 'uploaded_at')
