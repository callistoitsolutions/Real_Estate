from django.db import models


from datetime import date



from django.utils import timezone
from datetime import timedelta





class AutoLeadCapture(models.Model):
    name = models.CharField(max_length=100)
    property_id = models.CharField(max_length=20)
    source = models.CharField(max_length=30)
    inquiry_date = models.DateField()
    contact = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ManualLeadEntry(models.Model):
    name = models.CharField(max_length=100)
    requirement_type = models.CharField(max_length=20)
    budget = models.IntegerField()
    location = models.TextField()
    source = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class LeadAssignment(models.Model):
    lead_id = models.CharField(max_length=30)
    assignee = models.CharField(max_length=30)
    priority = models.CharField(max_length=20)
    followup_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.assignee

class LeadStatusUpdate(models.Model):
    lead_id = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    next_action = models.CharField(max_length=100)
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.status

class LeadAgeAnalysis(models.Model): 
    lead_id = models.CharField(max_length=30)
    created_date = models.DateField()
    last_update = models.DateField()
    days_old = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.days_old

class WalletTransaction(models.Model):
    user_id = models.CharField(max_length=30)
    transaction_type = models.CharField(max_length=10)
    amount = models.IntegerField()
    reason = models.CharField(max_length=100)
    balance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.amount

class WalletRecharge(models.Model):
    user_id = models.CharField(max_length=30)
    payment_mode = models.CharField(max_length=20)
    amount = models.IntegerField()
    transaction_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_mode


class LeadBuyRequest(models.Model):
    lead_id = models.CharField(max_length=30)
    agent_id = models.CharField(max_length=30)
    wallet_deduction = models.IntegerField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.wallet_deduction

class LeadHistory(models.Model):
    lead_id = models.CharField(max_length=30)
    activity_logs = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.activity_logs

class BulkLeadUpload(models.Model):
    file = models.FileField(upload_to='bulk_leads/')
    field_mapping = models.TextField()
    upload_date = models.DateField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.status




