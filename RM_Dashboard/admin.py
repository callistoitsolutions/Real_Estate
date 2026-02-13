# referrals/admin.py
from django.contrib import admin
from .models import AffiliateLink, ReferralVisit, ReferralConversion, CommissionRule, CommissionPayout

@admin.register(AffiliateLink)
class AffiliateLinkAdmin(admin.ModelAdmin):
    list_display = ('code','owner','created_by','target_type','target_id','click_count','registration_count','conversion_count','commission_total','active','created_at')
    search_fields = ('code','owner__username','owner__email')
    readonly_fields = ('click_count','registration_count','conversion_count','commission_total')

@admin.register(ReferralVisit)
class ReferralVisitAdmin(admin.ModelAdmin):
    list_display = ('affiliate','ip_address','created_at')
    search_fields = ('affiliate__code','ip_address')

@admin.register(ReferralConversion)
class ReferralConversionAdmin(admin.ModelAdmin):
    list_display = ('affiliate','user','order_id','amount','commission_amount','status','created_at')
    list_filter = ('status','created_at')
    search_fields = ('affiliate__code','user__username','order_id')

admin.site.register(CommissionRule)
admin.site.register(CommissionPayout)
