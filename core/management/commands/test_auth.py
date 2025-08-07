from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Test authentication with sample credentials'

    def handle(self, *args, **options):
        self.stdout.write('Testing authentication...')
        
        # Test admin authentication
        admin_user = authenticate(username='admin@cbt.com', password='admin123')
        if admin_user:
            self.stdout.write(self.style.SUCCESS(f'✓ Admin authentication successful: {admin_user.email}'))
            self.stdout.write(f'  - Username: {admin_user.username}')
            self.stdout.write(f'  - Email: {admin_user.email}')
            self.stdout.write(f'  - Is Staff: {admin_user.is_staff}')
            self.stdout.write(f'  - Is Admin: {admin_user.is_admin}')
        else:
            self.stdout.write(self.style.ERROR('✗ Admin authentication failed'))
        
        # Test student authentication
        student_user = authenticate(username='student@cbt.com', password='student123')
        if student_user:
            self.stdout.write(self.style.SUCCESS(f'✓ Student authentication successful: {student_user.email}'))
            self.stdout.write(f'  - Username: {student_user.username}')
            self.stdout.write(f'  - Email: {student_user.email}')
            self.stdout.write(f'  - Is Student: {student_user.is_student}')
        else:
            self.stdout.write(self.style.ERROR('✗ Student authentication failed'))
            
        # Check if users exist
        self.stdout.write('\nChecking user database:')
        for user in User.objects.all():
            self.stdout.write(f'  - {user.username} ({user.email}) - Active: {user.is_active}')
