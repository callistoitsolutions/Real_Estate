from django.db import models






class LeadPurchase(models.Model):
    lead_id = models.CharField(max_length=50)
    wallet_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lead {self.lead_id} - Deduction {self.wallet_deduction}"




class WalletRecharge(models.Model):
    PAYMENT_METHODS = [
        ("UPI", "UPI"),
        ("Credit/Debit", "Credit/Debit"),
        ("NetBanking", "NetBanking"),
        ("Cash", "Cash"),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recharge {self.amount} via {self.payment_method}"




class Commission(models.Model):
    lead_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commission {self.amount} for {self.lead_id}"



class SubscriptionPlan(models.Model):
    ROLE_CHOICES = [('Landlord','Landlord'), ('Agent','Agent'), ('Tenant','Tenant')]
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    features = models.TextField(help_text="Comma separated feature list")
    order = models.PositiveIntegerField(default=0)

    def feature_list(self):
        return [f.strip() for f in self.features.split(',') if f.strip()]

    def __str__(self):
        return f"{self.role} - {self.name}"

class FeatureComparison(models.Model):
    feature_name = models.CharField(max_length=200)
    free_value = models.CharField(max_length=100, blank=True)
    standard_value = models.CharField(max_length=100, blank=True)
    premium_value = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.feature_name
    
    
class UserSignup(models.Model):
    ROLE_CHOICES = [('Landlord','Landlord'), ('Agent','Agent'), ('Tenant','Tenant')]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    selected_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    # Dynamic fields stored as JSON or separate columns depending on role; here simplified
    full_name = models.CharField(max_length=150)
    property_type = models.CharField(max_length=100, blank=True)
    amenities = models.CharField(max_length=255, blank=True)
    agency_name = models.CharField(max_length=150, blank=True)
    service_areas = models.CharField(max_length=255, blank=True)
    preferred_locations = models.CharField(max_length=255, blank=True)
    move_in_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.role})"