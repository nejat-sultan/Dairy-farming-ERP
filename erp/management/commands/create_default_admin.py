# dairy_farm_erp/management/commands/create_default_admin.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError

from erp.models import UserProfile


class Command(BaseCommand):
    help = 'Creates a default admin user if not exists'

    def handle(self, *args, **kwargs):
        # try:
        #     admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'admin@admin')
        #     self.stdout.write(self.style.SUCCESS('Default admin user created successfully.'))
        # except IntegrityError:
        #     self.stdout.write(self.style.NOTICE('Default admin user already exists.'))
        try:
            admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'admin@admin')
            # Create the UserProfile entry without an employee
            UserProfile.objects.create(user=admin)
            self.stdout.write(self.style.SUCCESS('Default admin user created successfully.'))
        except IntegrityError:
            self.stdout.write(self.style.NOTICE('Default admin user already exists.'))
