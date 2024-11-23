from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(is_superuser=True).exists():
            # Automatically create a superuser if one doesn't exist
            User.objects.create_superuser(
                username='admin',
                email='admin@gmail.com',
                password='admin'  # Change this to a secure password
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists.'))
