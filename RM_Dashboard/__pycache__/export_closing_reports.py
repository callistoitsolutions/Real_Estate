from django.core.management.base import BaseCommand
from RM.models import ClosingReport
import csv
from io import StringIO

class Command(BaseCommand):
    help = "Export all closing reports to CSV"

    def handle(self, *args, **options):
        qs = ClosingReport.objects.select_related('referral','rm')
        out = StringIO()
        writer = csv.writer(out)
        writer.writerow(['ReferralID','RM','CommissionBeforeTax','Tax','FinalCommission','Status','PayoutDate'])
        for c in qs:
            writer.writerow([f"REF{c.referral.id}", c.rm.get_full_name() or c.rm.username, str(c.commission_before_tax), str(c.tax_amount), str(c.final_commission), c.status, c.payout_date or ''])
        print(out.getvalue())
