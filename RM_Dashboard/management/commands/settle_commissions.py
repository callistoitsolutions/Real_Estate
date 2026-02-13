# referrals/management/commands/settle_commissions.py
from django.core.management.base import BaseCommand
from referrals.models import ReferralConversion
from django.utils import timezone

class Command(BaseCommand):
    help = 'Settle pending commissions older than N days (example)'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=7)

    def handle(self, *args, **options):
        days = options['days']
        cutoff = timezone.now() - timezone.timedelta(days=days)
        pending = ReferralConversion.objects.filter(status='pending', created_at__lte=cutoff)
        count = pending.update(status='earned')
        self.stdout.write(self.style.SUCCESS(f'Settled {count} conversions'))
