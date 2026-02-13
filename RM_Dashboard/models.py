from django.db import models
from django.db import models

from django.conf import settings



# Create your models here.
class LeadStatus(models.Model):
    lead_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    next_action = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lead {self.lead_id} - Status {self.status}"
    
    

from django.utils import timezone

class LeadNote(models.Model):
    lead_id = models.CharField(max_length=50)   # e.g. LEAD7343
    note_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Note for {self.lead_id} - {self.note_text[:30]}"



class LeadReassignment(models.Model):
    lead_id = models.CharField(max_length=50)   # e.g. LEAD7343
    new_user = models.CharField(max_length=100) # Agent/RM name or ID
    reassigned_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Lead {self.lead_id} reassigned to {self.new_user}"
    
    


class CommissionClaim(models.Model):
    lead_id = models.CharField(max_length=50)   # Example: L001
    agent_id = models.CharField(max_length=50)  # Example: AG001
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    claimed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Claim by {self.agent_id} for Lead {self.lead_id} - ₹{self.amount}"












# referrals/models.py

import uuid

User = settings.AUTH_USER_MODEL

class AffiliateLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, related_name='affiliate_links', on_delete=models.CASCADE)   # RM / user who owns the link
    created_by = models.ForeignKey(User, related_name='affiliate_links_created', on_delete=models.SET_NULL, null=True, blank=True)  # admin or RM who created it
    code = models.CharField(max_length=64, unique=True)  # referral code
    target_type = models.CharField(max_length=50, choices=[('subscription','subscription'),('addon','addon'),('product','product')], default='subscription')
    target_id = models.CharField(max_length=128, blank=True, null=True)
    click_count = models.PositiveIntegerField(default=0)
    registration_count = models.PositiveIntegerField(default=0)
    conversion_count = models.PositiveIntegerField(default=0)
    commission_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.owner} - {self.code}"

    def get_target_url(self):
        # returns the relative URL that the referral should send people to
        if self.target_type == 'subscription' and self.target_id:
            return f"/subscription/{self.target_id}/?ref={self.code}"
        return f"/register/?ref={self.code}"

class ReferralVisit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    affiliate = models.ForeignKey(AffiliateLink, related_name='visits', on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    referer = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

class ReferralConversion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    affiliate = models.ForeignKey(AffiliateLink, related_name='conversions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='referred_by_user', on_delete=models.SET_NULL, null=True, blank=True)
    order_id = models.CharField(max_length=128, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[('pending','pending'),('earned','earned'),('paid','paid'),('reversed','reversed')], default='pending')
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)

class CommissionRule(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    target_type = models.CharField(max_length=50, choices=[('subscription','subscription'),('addon','addon'),('product','product')])
    fixed_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    prefer_max = models.BooleanField(default=False)  # if True pick max(fixed, percent)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CommissionPayout(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    affiliate = models.ForeignKey(AffiliateLink, related_name='payouts', on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_on = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('requested','requested'),('done','done'),('rejected','rejected')], default='requested')
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payout {self.affiliate.code} - {self.total_amount} - {self.status}"
