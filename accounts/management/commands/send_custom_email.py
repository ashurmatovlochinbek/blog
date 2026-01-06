# In Django shell (python manage.py shell)
from django.core.mail import send_mail

# accounts/management/commands/send_custom_email.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Send a test email'

    def handle(self, *args, **options):
        try:
            result = send_mail(
                'Test Subject',
                'Test message.',
                'l10.ashurmatov@gmail.com',
                ['pizza.lovers.uz@gmail.com'],  # Change this to your test email
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Email sent successfully: {result}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error sending email: {e}'))
            import traceback
            traceback.print_exc()