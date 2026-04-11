from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

from seo.models import LocationSEO
from Admin_App.models import *
from Main_App.models import *

# ---------------- Helper functions ----------------
def generate_sponsored_ad_seo(instance):
    """Generates meta title, description, and keywords for SponsoredAd"""
    base_title = f"{instance.title} | {instance.business_name}"
    meta_title = (base_title[:117] + "...") if len(base_title) > 120 else base_title
    meta_description = f"{instance.description[:190]}..." if len(instance.description) > 200 else instance.description
    keywords = ' '.join([
        w for w in (instance.title + ' ' + instance.description + ' ' + instance.business_name).lower().split()
        if len(w) > 3 and w.isalnum()
    ])
    return meta_title, meta_description, keywords

def generate_residential_faq(instance):
    instance.faqs.all().delete()
    faqs = [
        ("What is the built-up area of the property?",
         f"The built-up area of this residential property is {instance.builtup_area} sq.ft."),
        ("How many bedrooms and bathrooms are available?",
         f"It has {instance.bedrooms} bedrooms and {instance.bathrooms} bathrooms."),
        ("What is the furnishing status?",
         f"The property is {instance.furnishing}."),
        ("Which floor is the property located on?",
         f"The property is on floor {instance.floor_no} of {instance.total_floors} floors."),
        ("What is the monthly rent?",
         f"The monthly rent is ₹{instance.rent_price}."),
        ("How much is the security deposit?",
         f"The security deposit is ₹{instance.security_deposit}."),
    ]
    for q, a in faqs:
        PropertyFAQ.objects.create(residential=instance, question=q, answer=a)

def generate_commercial_faq(instance):
    instance.faqs.all().delete()
    faqs = [
        ("What is the built-up and carpet area?",
         f"This commercial unit has a built-up area of {instance.builtup_area} sq.ft and a carpet area of {instance.carpet_area} sq.ft."),
        ("What is the expected monthly rent?",
         f"The expected rent is ₹{instance.expected_rent}."),
        ("How many parking spaces are available?",
         f"{instance.private_parking} private and {instance.public_parking} public parking spaces are available."),
        ("Is this suitable for commercial/office use?",
         f"Yes, this is a {instance.property_type} suitable for business and office use."),
        ("Which floor is the property located on?",
         f"It is located on floor {instance.your_no} of {instance.total_floors} floors."),
    ]
    for q, a in faqs:
        PropertyFAQ.objects.create(commercial=instance, question=q, answer=a)

def generate_pg_faq(instance):
    instance.faqs.all().delete()
    faqs = [
        ("What is the rent for this PG?",
         f"The monthly rent is ₹{instance.rent_price}."),
        ("Is food included?",
         "Yes, meals are included." if instance.meals_included else "Meals are not included."),
        ("What is the sharing type?",
         f"The sharing type offered is {instance.sharing_type}."),
        ("What is the furnishing type?",
         f"The property is {instance.furnishing_type} furnished."),
        ("Is there a security deposit?",
         f"Security deposit is ₹{instance.security_deposit}."),
    ]
    for q, a in faqs:
        PropertyFAQ.objects.create(pg=instance, question=q, answer=a)

# ---------------- Templates ----------------
templates = {
    "blog": {
        "title": "Blog: {title} | Property Tips & Real Estate Insights",
        "desc": "Read expert insights on {title}. Stay updated with the latest property market trends and rental advice.",
        "primary": "{title} rental tips",
        "secondary": "real estate blog, home renting, property management",
    },
    "service": {
        "title": "{title} | Professional Property Services",
        "desc": "Our {title} service helps you with {short}. Discover how we simplify real estate for you.",
        "primary": "{title} service",
        "secondary": "property service, home rental, estate agency, property management",
    },
    "ad": {
        "title": "{title} | {category} Offers & Promotions",
        "desc": "Check out our latest ad: {title}. {short}. Explore deals and offers on real estate and rentals.",
        "primary": "{title} offer",
        "secondary": "property ad, real estate deals, rental promotions, {category}",
    },
    "residential": {
        "title": "{property_title} in {city} | Residential Property for Rent",
        "desc": "Explore {property_title} located in {area}, {city}. Rent: ₹{rent_price}, Bedrooms: {bedrooms}, Bathrooms: {bathrooms}.",
        "primary": "{property_title} for rent",
        "secondary": "residential property, rent in {city}, {area}, apartments, flats",
    },
    "commercial": {
        "title": "{property_type} in {city} - {area_locality} | Commercial Space for Rent",
        "desc": "Looking for {property_type} in {area_locality}, {city}? Rent: ₹{expected_rent}. Builtup area: {builtup_area} sqft.",
        "primary": "{property_type} rental",
        "secondary": "commercial property, office space, retail space, {city}",
    },
    "pg": {
        "title": "PG/Co-living: {property_type} in {city} | Rent ₹{rent_price}",
        "desc": "Find PG/Co-living spaces in {area_locality}, {city}. Rent: ₹{rent_price}, Sharing: {sharing_type}, Furnishing: {furnishing_type}.",
        "primary": "{property_type} in {city}",
        "secondary": "PG for rent, co-living, {city}, {area_locality}",
    },
    "addon": {
        "title": "{name} | Premium Add-On Service",
        "desc": "Enhance your experience with our {name} add-on. {short}. Available for {roles}.",
        "primary": "{name} add-on service",
        "secondary": "subscription addons, premium service, {roles}",
    },
    "sponsored_ad": {
        "title": "{title} | {business_name} Sponsored Offer",
        "desc": "Discover our sponsored promotion: {title}. {short}. Check deals and offers from {business_name}.",
        "primary": "{title} sponsored ad",
        "secondary": "sponsored ad, property promotion, real estate deals, {business_name}",
    },
}

# ---------------- Create SEO Page ----------------
def create_seo_page(instance, template_key):
    key = f"{template_key}-{slugify(str(instance))}"
    if LocationSEO.objects.filter(key=key).exists():
        return

    kwargs = {}

    if template_key in ["blog", "service", "ad", "residential", "commercial", "pg", "addon", "sponsored_ad"]:
        template = templates[template_key]
        # Build kwargs dynamically
        if template_key == "blog":
            kwargs = {
                "meta_title": template["title"].format(title=instance.title),
                "meta_description": template["desc"].format(title=instance.title),
                "primary_keyword": template["primary"].format(title=instance.title),
                "secondary_keywords": template["secondary"],
                "intro_html": f"<h2>{instance.title}</h2><p>{getattr(instance, 'content', '')[:200]}...</p>",
            }
        elif template_key == "service":
            kwargs = {
                "meta_title": template["title"].format(title=instance.title),
                "meta_description": template["desc"].format(title=instance.title, short=instance.short_description[:150]),
                "primary_keyword": template["primary"].format(title=instance.title),
                "secondary_keywords": template["secondary"],
                "intro_html": f"<h2>{instance.title}</h2><p>{instance.short_description}</p>",
            }
        elif template_key == "ad":
            kwargs = {
                "meta_title": template["title"].format(title=instance.title, category=instance.category),
                "meta_description": template["desc"].format(title=instance.title, short=instance.short_description[:150], category=instance.category),
                "primary_keyword": template["primary"].format(title=instance.title),
                "secondary_keywords": template["secondary"].format(category=instance.category),
                "intro_html": f"<h2>{instance.title}</h2><p>Category: {instance.category}</p><p>{instance.short_description}</p>",
            }
        elif template_key == "residential":
            kwargs = {
                "meta_title": template["title"].format(property_title=instance.property_title, city=instance.city),
                "meta_description": template["desc"].format(property_title=instance.property_title, city=instance.city, area=instance.area, rent_price=instance.rent_price, bedrooms=instance.bedrooms, bathrooms=instance.bathrooms),
                "primary_keyword": template["primary"].format(property_title=instance.property_title),
                "secondary_keywords": template["secondary"].format(city=instance.city, area=instance.area),
                "intro_html": f"<h2>{instance.property_title} - {instance.city}</h2><p>Area: {instance.area}, Bedrooms: {instance.bedrooms}, Bathrooms: {instance.bathrooms}, Rent: ₹{instance.rent_price}</p>",
            }
        elif template_key == "commercial":
            kwargs = {
                "meta_title": template["title"].format(property_type=instance.property_type, city=instance.city, area_locality=instance.area_locality),
                "meta_description": template["desc"].format(property_type=instance.property_type, city=instance.city, area_locality=instance.area_locality, expected_rent=instance.expected_rent, builtup_area=instance.builtup_area),
                "primary_keyword": template["primary"].format(property_type=instance.property_type),
                "secondary_keywords": template["secondary"].format(city=instance.city),
                "intro_html": f"<h2>{instance.property_type} in {instance.city}</h2><p>Area: {instance.area_locality}, Rent: ₹{instance.expected_rent}, Builtup Area: {instance.builtup_area} sqft</p>",
            }
        elif template_key == "pg":
            kwargs = {
                "meta_title": template["title"].format(property_type=instance.property_type, city=instance.city, rent_price=instance.rent_price),
                "meta_description": template["desc"].format(property_type=instance.property_type, city=instance.city, area_locality=instance.area_locality, rent_price=instance.rent_price, sharing_type=instance.sharing_type, furnishing_type=instance.furnishing_type),
                "primary_keyword": template["primary"].format(property_type=instance.property_type, city=instance.city),
                "secondary_keywords": template["secondary"].format(city=instance.city, area_locality=instance.area_locality),
                "intro_html": f"<h2>{instance.property_type} in {instance.city}</h2><p>Area: {instance.area_locality}, Sharing: {instance.sharing_type}, Furnishing: {instance.furnishing_type}, Rent: ₹{instance.rent_price}</p>",
            }
        elif template_key == "addon":
            kwargs = {
                "meta_title": template["title"].format(name=instance.name),
                "meta_description": template["desc"].format(
                    name=instance.name,
                    short=instance.description[:150],
                    roles=instance.applicableroles or "all users",
                ),
                "primary_keyword": template["primary"].format(name=instance.name),
                "secondary_keywords": template["secondary"].format(
                    roles=instance.applicableroles or "all users"
                ),
                "intro_html": f"<h2>{instance.name}</h2><p>{instance.description}</p><p><strong>Price:</strong> ₹{instance.price}</p>",
            }
        elif template_key == "sponsored_ad":
            kwargs = {
                "meta_title": template["title"].format(title=instance.title, business_name=instance.business_name),
                "meta_description": template["desc"].format(title=instance.title, short=instance.description[:150], business_name=instance.business_name),
                "primary_keyword": template["primary"].format(title=instance.title),
                "secondary_keywords": template["secondary"].format(business_name=instance.business_name),
                "intro_html": f"""
                    <h2>{instance.title}</h2>
                    <p>{instance.description}</p>
                    <p><strong>Business:</strong> {instance.business_name}</p>
                    <a href="{instance.contact_url}" target="_blank" rel="nofollow sponsored">Visit</a>
                """,
            }

    LocationSEO.objects.create(
        key=key,
        pagetype=template_key,
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.id,
        is_active=False,
        **kwargs
    )

# ---------------- Receivers ----------------
@receiver(post_save, sender=Blog)
def blog_post_save(sender, instance, created, **kwargs):
    if created:
        create_seo_page(instance, "blog")

@receiver(post_save, sender=Service)
def service_post_save(sender, instance, created, **kwargs):
    if created:
        create_seo_page(instance, "service")

@receiver(post_save, sender=Ad)
def ad_post_save(sender, instance, created, **kwargs):
    if created:
        create_seo_page(instance, "ad")



@receiver(post_save, sender=ResidentialProperty)
def residential_post_save(sender, instance, created, **kwargs):
    if created:
        create_seo_page(instance, "residential")
        generate_residential_faq(instance)

@receiver(post_save, sender=CommercialProperty)
def commercial_post_save(sender, instance, created, **kwargs):
    if created:
        create_seo_page(instance, "commercial")
        generate_commercial_faq(instance)

@receiver(post_save, sender=PGProperty)
def pg_post_save(sender, instance, created, **kwargs):
    if created:
        create_seo_page(instance, "pg")
        generate_pg_faq(instance)


