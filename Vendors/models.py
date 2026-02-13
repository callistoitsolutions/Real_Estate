from django.db import models
from django.utils import timezone

VENDOR_STATUS_CHOICES = [
    ('normal', 'Normal'),
    ('verified', 'Verified'),
    ('featured', 'Featured'),
    ('sponsored', 'Sponsored'),
]

PRICING_MODEL_CHOICES = [
    ('flat', 'Flat'),
    ('km_based', 'Per km'),
    ('hourly', 'Hourly'),
    ('custom', 'Custom'),
]


class Vendor(models.Model):
    business_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    primary_service = models.CharField(max_length=100)
    service_mode = models.CharField(max_length=10, choices=[('single','Single'),('multi','Multi')], default='single')
    services = models.JSONField(blank=True, default=list)  # list of services when multiservice selected
    special_tags = models.CharField(max_length=300, blank=True)

    city = models.CharField(max_length=120)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    company_reg_no = models.CharField(max_length=100, blank=True, null=True)
    exp_year = models.PositiveIntegerField(default=0)
    service_description = models.TextField(blank=True)

    coverage_km = models.PositiveIntegerField(default=25)
    pricing_model = models.CharField(max_length=20, choices=PRICING_MODEL_CHOICES, default='flat')
    price_flat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    bank_account = models.CharField(max_length=200, blank=True)

    logo = models.ImageField(upload_to='vendor_logos/', blank=True, null=True)
    vendor_status = models.CharField(max_length=20, choices=VENDOR_STATUS_CHOICES, default='normal')
    
   # Performance Metrics
    commission_rate = models.FloatField(null=True, blank=True, help_text="Vendor share % (60 = 60%)")
    cumulative_revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_leads = models.PositiveIntegerField(default=0)
    accepted_leads = models.PositiveIntegerField(default=0)

    is_inhouse = models.BooleanField(default=False)
    is_rm_candidate = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


# Performance Metrics



    # convenience
    def is_verified(self):
        return self.vendor_status == 'verified'

    def is_featured(self):
        return self.vendor_status == 'featured'

    def is_sponsored(self):
        return self.vendor_status == 'sponsored'

    def __str__(self):
        return f"{self.business_name} ({self.city})"


class VendorDocument(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='vendor_docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doc for {self.vendor.business_name} - {self.file.name}"





# vendors_module/models.py
# (or place in vendors_module/enquiry_models.py and import accordingly)

from django.conf import settings


class ServiceEnquiry(models.Model):
    STATUS_CHOICES = [
        ('new','New'),
        ('shared','Shared'),
        ('assigned','Assigned'),
        ('no_response','No Response'),
        ('completed','Completed'),
        ('cancelled','Cancelled'),
    ]

    enquiry_id = models.CharField(max_length=64, unique=True)

    # NEW FIELDS (Customer details)
    customer_name = models.CharField(max_length=150,default="")
    customer_mobile = models.CharField(max_length=20,default="")

    # Service details
    service = models.CharField(max_length=120)
    city = models.CharField(max_length=120)

    # NEW FIELDS (Pickup / Drop / Notes)
    pickup_address = models.TextField(blank=True)
    drop_address = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    details = models.TextField(blank=True)  # optional old field

    preferred_dt = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    # Sharing / assignment
    shared_vendors = models.JSONField(blank=True, default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    assigned_vendor = models.ForeignKey(
        Vendor,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_enquiries'
    )

    expires_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.enquiry_id} — {self.service} ({self.city})"



    
    
class LeadShare(models.Model):
    """
    Record each time a lead/enquiry is shared to a vendor.
    This helps tracking lead distribution & responses.
    """
    enquiry = models.ForeignKey(ServiceEnquiry, on_delete=models.CASCADE, related_name='lead_shares')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='lead_shares')
    shared_at = models.DateTimeField(default=timezone.now)
    responded = models.BooleanField(default=False)
    accepted = models.BooleanField(null=True)  # True accept, False reject, None not responded
    response_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.enquiry.enquiry_id} -> {self.vendor.business_name}"
    
    


class CommissionLedger(models.Model):
    enquiry = models.OneToOneField('ServiceEnquiry', on_delete=models.CASCADE, related_name='commission')
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vendor_share = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    platform_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)  # whether vendor has been paid (full)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # cumulative paid amount

    # optional: which user (internal RM) got this lead (extracted from enquiry.created_by or set by admin)
    assigned_rm = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='rm_commissions')

    def outstanding(self):
        return max(self.total_amount - self.vendor_share - self.paid_amount, 0)

    def __str__(self):
        return f"Commission for {self.enquiry.enquiry_id} / {self.vendor.business_name}"





class CommissionTransaction(models.Model):
    """
    Records payments and adjustments related to CommissionLedger.
    One CommissionLedger per enquiry (OneToOne), but there may be multiple transactions (partial payments).
    """
    ledger = models.ForeignKey('CommissionLedger', on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text='Amount paid to vendor in this transaction')
    paid_to_vendor = models.BooleanField(default=False)  # True if vendor paid
    paid_to_platform = models.BooleanField(default=False)  # True if platform settlement recorded
    paid_at = models.DateTimeField(null=True, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Txn {self.id} for {self.ledger.enquiry.enquiry_id} : {self.amount}"