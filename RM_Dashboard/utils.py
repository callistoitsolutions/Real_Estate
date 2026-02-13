# referrals/utils.py
import secrets
from decimal import Decimal
from .models import CommissionRule

def make_code(prefix='RM'):
    token = secrets.token_urlsafe(6)  # short random token
    return f"{prefix}-{token}"

def calculate_commission_for(affiliate_link, amount_decimal):
    """
    Calculate commission using CommissionRule for the affiliate_link.target_type.
    amount_decimal should be Decimal or numeric convertible to Decimal.
    """
    rule = CommissionRule.objects.filter(target_type=affiliate_link.target_type, active=True).first()
    if not rule:
        return Decimal('0')
    fixed = Decimal(rule.fixed_amount or 0)
    percent = (Decimal(rule.percent or 0) * Decimal(amount_decimal) / Decimal('100'))
    if rule.prefer_max:
        return max(fixed, percent)
    return fixed + percent
