from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Reset demo user passwords'

    def handle(self, *args, **options):
        # Update admin password
        try:
            admin = User.objects.get(email='admin@cbt.com')
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Updated admin password'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Admin user not found'))

        # Update student password  
        try:
            student = User.objects.get(email='student@cbt.com')
            student.set_password('student123')
            student.save()
            self.stdout.write(self.style.SUCCESS(f'Updated student password'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Student user not found'))
            
        self.stdout.write(self.style.SUCCESS('Credentials:'))
        self.stdout.write('Admin: admin@cbt.com / admin123')
        self.stdout.write('Student: student@cbt.com / student123')
