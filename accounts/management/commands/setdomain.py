# accounts/management/commands/set_site_domain.py
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Set the site domain based on DEBUG setting'

    def handle(self, *args, **options):
        site = Site.objects.get(id=settings.SITE_ID)
        site.domain = settings.DEFAULT_DOMAIN
        site.name = 'Blog Project' if not settings.DEBUG else 'Blog Project (Dev)'
        site.save()

        self.stdout.write(
            self.style.SUCCESS(f'Successfully set site domain to: {site.domain}')
        )