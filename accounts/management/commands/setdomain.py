from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
import os

class Command(BaseCommand):
    help = 'Sets the site domain'

    def handle(self, *args, **options):
        domain = os.environ.get('SITE_DOMAIN', 'blog-jo8c.onrender.com')
        site = Site.objects.get(id=1)
        site.domain = domain
        site.name = 'My Blog'
        site.save()
        self.stdout.write(self.style.SUCCESS(f'Site domain set to: {domain}'))