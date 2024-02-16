# your_app/management/commands/seed_admin.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seed database with initial admin user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Admin username')
        parser.add_argument('email', type=str, help='Admin email')
        parser.add_argument('password', type=str, help='Admin password')
    def handle(self, *args, **options):
        user_name = options["username"]
        email = options["email"]
        password = options["password"]
        if not User.objects.filter(username=user_name).exists():
            User.objects.create_superuser(password, email, password)
            self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
