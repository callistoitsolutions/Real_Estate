from django.db import models
from datetime import date

class Property(models.Model):
    # Basic Property Details
    property_title = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    property_address = models.TextField()
    property_type = models.CharField(max_length=50)
    builtup_area = models.FloatField()
    carpet_area = models.FloatField()
    zone = models.CharField(max_length=50)
    society_type = models.CharField(max_length=50)
    recommended_for = models.CharField(max_length=255)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    balconies = models.IntegerField()
    furnishing = models.CharField(max_length=50)
    floor_no = models.IntegerField()
    total_floors = models.IntegerField()
    age_of_property = models.IntegerField()
    water_type = models.CharField(max_length=50)

    # Rent Details
    rent_price = models.FloatField()
    security_deposit = models.FloatField()
    maintenance = models.FloatField(default=0)

    # Featured & Verified
    is_featured = models.CharField(max_length=10, blank=True, null=True)
    featured_days = models.IntegerField(blank=True, null=True)
    manual_featured_days = models.IntegerField(blank=True, null=True)
    featured_start_date = models.DateField(blank=True, null=True)
    featured_end_date = models.DateField(blank=True, null=True)
    service_amount = models.FloatField(blank=True, null=True)
    placement = models.CharField(max_length=50, blank=True, null=True)
    is_verified = models.CharField(max_length=10, blank=True, null=True)

    # Files
    property_images = models.FileField(upload_to='property_images/', blank=True, null=True)
    floor_plan = models.FileField(upload_to='floor_plans/', blank=True, null=True)
    upload_registry = models.FileField(upload_to='documents/', blank=True, null=True)
    upload_house_tax = models.FileField(upload_to='documents/', blank=True, null=True)
    upload_utility_bill = models.FileField(upload_to='documents/', blank=True, null=True)
    upload_aadhar = models.FileField(upload_to='documents/', blank=True, null=True)
    upload_pan = models.FileField(upload_to='documents/', blank=True, null=True)
    upload_index2 = models.FileField(upload_to='documents/', blank=True, null=True)

    # Brokerage
    brokerage_applicable = models.CharField(max_length=10, blank=True, null=True)
    brokerage_payer = models.CharField(max_length=50, blank=True, null=True)
    brokerage_type = models.CharField(max_length=50, blank=True, null=True)
    brokerage_value = models.FloatField(blank=True, null=True)
    percentage_extra = models.FloatField(blank=True, null=True)
    brokerage_description = models.TextField(blank=True, null=True)

    # New Fields
    exclusive_property = models.BooleanField(default=False)
    upload_video = models.BooleanField(default=False)
    video_url = models.URLField(blank=True, null=True)
    video_from = models.DateField(blank=True, null=True)
    video_to = models.DateField(blank=True, null=True)
    video_platforms = models.CharField(max_length=255, blank=True, null=True)  # comma separated platforms
    
    nearby_facilities = models.CharField(max_length=255, blank=True, null=True)  # comma separated
    amenities = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return self.property_title





class CommercialProperty(models.Model):
    # --- Basic Details ---
    property_type = models.CharField(max_length=100, default="Not Specified")
    city = models.CharField(max_length=100)
    area_locality = models.CharField(max_length=200)
    property_address = models.TextField()
    building_name = models.CharField(max_length=200, blank=True, null=True)
    possession_status = models.CharField(max_length=100, blank=True, null=True)
    age_of_property = models.IntegerField(default=0)
    zone_type = models.CharField(max_length=100, blank=True, null=True)
    location_hub = models.CharField(max_length=150, blank=True, null=True)
    property_condition = models.CharField(max_length=150, blank=True, null=True)
    ownership_type = models.CharField(max_length=150, blank=True, null=True)
    construction_status = models.CharField(max_length=150, blank=True, null=True)

    # --- Property Details ---
    builtup_area = models.IntegerField(default=0)
    carpet_area = models.IntegerField(default=0)
    total_floors = models.IntegerField(default=0)
    your_no = models.IntegerField(default=0)   # floor no
    no_of_staircase = models.IntegerField(default=0)
    passenger_lifts = models.IntegerField(default=0)
    service_lifts = models.IntegerField(default=0)
    private_parking = models.IntegerField(default=0)
    public_parking = models.IntegerField(default=0)
    minimum_seats = models.IntegerField(default=0)
    maximum_seats = models.IntegerField(default=0)
    number_of_cabin = models.IntegerField(default=0)
    meeting_room = models.IntegerField(default=0)
    floring_type = models.CharField(max_length=150, blank=True, null=True)

    # --- Rent Details ---
    expected_rent = models.FloatField(default=0)
    security_deposit = models.FloatField(default=0)
    maintenance_charges = models.FloatField(default=0)
    rent_available_from = models.DateField(blank=True, null=True)
    lock_in_period = models.IntegerField(default=0)
    rent_increase = models.FloatField(default=0.0)

    # --- Uploads ---
    property_images = models.FileField(upload_to="property/images/", blank=True, null=True)
    floor_plan = models.FileField(upload_to="property/floor_plans/", blank=True, null=True)

    # --- Featured & Verified ---
    is_featured = models.BooleanField(default=False)
    featured_days = models.IntegerField(blank=True, null=True)
    manual_featured_days = models.IntegerField(blank=True, null=True)
    featured_start_date = models.DateField(blank=True, null=True)
    featured_end_date = models.DateField(blank=True, null=True)
    service_amount = models.FloatField(default=0.0)
    placement = models.CharField(max_length=50, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    # --- Documents ---
    upload_registry = models.FileField(upload_to="property/docs/", blank=True, null=True)
    upload_house_tax = models.FileField(upload_to="property/docs/", blank=True, null=True)
    upload_utility_bill = models.FileField(upload_to="property/docs/", blank=True, null=True)
    upload_aadhar = models.FileField(upload_to="property/docs/", blank=True, null=True)
    upload_pan = models.FileField(upload_to="property/docs/", blank=True, null=True)
    upload_index2 = models.FileField(upload_to="property/docs/", blank=True, null=True)

    # --- Brokerage ---
    brokerage_applicable = models.CharField(max_length=10, default="No")   # Yes/No
    brokerage_payer = models.CharField(max_length=50, blank=True, null=True)
    brokerage_type = models.CharField(max_length=50, blank=True, null=True)
    brokerage_value = models.FloatField(default=0.0)
    percentage_extra = models.FloatField(default=0.0)
    brokerage_description = models.TextField(blank=True, null=True)

    # --- Exclusive & Video ---
    exclusive_property = models.BooleanField(default=False)
    upload_video = models.BooleanField(default=False)
    video_url = models.URLField(blank=True, null=True)
    video_from = models.DateField(blank=True, null=True)
    video_to = models.DateField(blank=True, null=True)
    video_platforms = models.CharField(max_length=200, blank=True, null=True)

    # --- Facilities & Amenities ---
    nearby_facilities = models.TextField(blank=True, null=True)
    amenities = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.property_type} in {self.city} - {self.area_locality}"





class PG_Property(models.Model):
    # Basic details
    property_type = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    area_locality = models.CharField(max_length=200)
    address = models.TextField()
    furnishing_type = models.CharField(max_length=50)
    sharing_type = models.CharField(max_length=50)
    meals_included = models.BooleanField(default=False)
    meal_type = models.CharField(max_length=50, blank=True, null=True)
    minimum_stay = models.IntegerField()
    available_from = models.DateField()

    # Rent details
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)

    # Images / Documents
    property_images = models.FileField(upload_to="property_images/", blank=True, null=True)
    floor_plan = models.FileField(upload_to="floor_plans/", blank=True, null=True)

    # Featured & verified
    is_featured = models.CharField(max_length=10, choices=[("Yes", "Yes"), ("No", "No")], default="No")
    featured_days = models.IntegerField(blank=True, null=True)
    manual_featured_days = models.IntegerField(blank=True, null=True)
    featured_start_date = models.DateField(blank=True, null=True)
    featured_end_date = models.DateField(blank=True, null=True)
    service_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    placement = models.CharField(max_length=50, blank=True, null=True)
    is_verified = models.CharField(max_length=10, choices=[("yes", "Yes"), ("no", "No")], default="no")

    # Verification docs
    upload_registry = models.FileField(upload_to="docs/", blank=True, null=True)
    upload_house_tax = models.FileField(upload_to="docs/", blank=True, null=True)
    upload_utility_bill = models.FileField(upload_to="docs/", blank=True, null=True)
    upload_aadhar = models.FileField(upload_to="docs/", blank=True, null=True)
    upload_pan = models.FileField(upload_to="docs/", blank=True, null=True)
    upload_index2 = models.FileField(upload_to="docs/", blank=True, null=True)

    # Brokerage
    brokerage_applicable = models.CharField(max_length=10, blank=True, null=True)
    brokeragePayer = models.CharField(max_length=50, blank=True, null=True)
    brokerageType = models.CharField(max_length=50, blank=True, null=True)
    brokerageValue = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    percentageExtra = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    brokerageDescription = models.TextField(blank=True, null=True)

    # Exclusive property
    exclusive_property = models.BooleanField(default=False)

    # Video
    upload_video = models.BooleanField(default=False)
    video_url = models.URLField(blank=True, null=True)
    video_from = models.DateField(blank=True, null=True)
    video_to = models.DateField(blank=True, null=True)
    video_platforms = models.CharField(max_length=200, blank=True, null=True)

    # Facilities & Amenities
    nearby_facilities = models.CharField(max_length=200, blank=True, null=True)
    amenities = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property_type} - {self.city}"



class BoostListing(models.Model):
    boost_type = models.CharField(max_length=20)
    boost_duration = models.IntegerField()
    listing_id = models.IntegerField()  # or ForeignKey if property listing model available
    payment_method = models.CharField(max_length=20)
    agree_terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.boost_type} - {self.listing_id}"


class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.phone}"
