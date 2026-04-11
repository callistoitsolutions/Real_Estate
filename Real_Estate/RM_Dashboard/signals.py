# referrals/signals.py
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import AffiliateLink, ReferralConversion
from .utils import calculate_commission_for
from decimal import Decimal

# If you have an Order model, adapt the import below, e.g. from orders.models import Order
try:
    from orders.models import Order

    @receiver(post_save, sender=Order)
    def order_post_save(sender, instance, created, **kwargs):
        # Trigger only when order is paid. Adjust status field name/value per your project.
        if getattr(instance, 'status', None) != 'paid':
            return

        request = getattr(instance, '_request_cache', None)
        ref_code = None
        if request:
            ref_code = request.POST.get('referral_code') or request.session.get('referral_code')
        # fallback: if you stored referral_code on the order row
        if not ref_code and getattr(instance, 'referral_code', None):
            ref_code = instance.referral_code
        if not ref_code:
            return
        try:
            aff = AffiliateLink.objects.get(code=ref_code, active=True)
        except AffiliateLink.DoesNotExist:
            return
        amount = Decimal(getattr(instance, 'total_amount', 0) or 0)
        comm = calculate_commission_for(aff, amount)
        ReferralConversion.objects.create(
            affiliate=aff,
            user=getattr(instance, 'user', None),
            order_id=str(instance.pk),
            amount=amount,
            commission_amount=comm,
            status='pending'
        )
        AffiliateLink.objects.filter(pk=aff.pk).update(
            registration_count=models.F('registration_count')+1,
            conversion_count=models.F('conversion_count')+1,
            commission_total=models.F('commission_total')+comm
        )
except Exception:
    # If your project doesn't have orders.Order, ignore; use checkout logic instead.
    pass
