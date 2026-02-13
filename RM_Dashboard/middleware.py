# referrals/middleware.py
from django.utils.deprecation import MiddlewareMixin
from .models import AffiliateLink, ReferralVisit
from django.db import models

class ReferralMiddleware(MiddlewareMixin):
    """
    Capture ?ref=CODE on any request, log visits, increment counts, and store in session.
    """
    def process_request(self, request):
        ref = request.GET.get('ref') or request.COOKIES.get('referral')
        if not ref:
            return
        try:
            aff = AffiliateLink.objects.get(code=ref, active=True)
        except AffiliateLink.DoesNotExist:
            return
        # increment click_count atomically
        AffiliateLink.objects.filter(pk=aff.pk).update(click_count=models.F('click_count')+1)
        # log visit
        ReferralVisit.objects.create(
            affiliate=aff,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT',''),
            referer=request.META.get('HTTP_REFERER','')
        )
        # store referral code in session for later
        request.session['referral_code'] = ref

    def process_response(self, request, response):
        try:
            ref = request.session.get('referral_code')
            if ref and not request.COOKIES.get('referral'):
                response.set_cookie('referral', ref, max_age=60*60*24*30, samesite='Lax')
        except Exception:
            pass
        return response
