from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()

class Command(BaseCommand):
    help = 'Test password reset functionality'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email address to test password reset')

    def handle(self, *args, **options):
        email = options.get('email', 'test@ntech.com')
        
        self.stdout.write('🔐 Testing Password Reset Functionality...')
        
        try:
            user = User.objects.get(email=email, is_active=True)
            self.stdout.write(f'✅ Found user: {user.email}')
            
            # Generate reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            self.stdout.write(f'🎯 Password Reset Details:')
            self.stdout.write(f'   • User: {user.get_full_name()} ({user.email})')
            self.stdout.write(f'   • Account Type: {user.get_user_type_display()}')
            self.stdout.write(f'   • UID: {uid}')
            self.stdout.write(f'   • Token: {token[:20]}...')
            
            # Generate reset URL
            reset_url = f'http://127.0.0.1:8000/authentication/password-reset/confirm/{uid}/{token}/'
            self.stdout.write(f'🔗 Reset URL: {reset_url}')
            
            self.stdout.write(self.style.SUCCESS('\n✅ Password reset test completed!'))
            self.stdout.write('📝 To test:')
            self.stdout.write(f'   1. Go to: http://127.0.0.1:8000/authentication/password-reset/')
            self.stdout.write(f'   2. Enter email: {email}')
            self.stdout.write(f'   3. Check console for email (in development mode)')
            self.stdout.write(f'   4. Or use direct reset URL above')
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ User with email {email} not found'))
            self.stdout.write('Available test users:')
            for user in User.objects.filter(is_active=True)[:5]:
                self.stdout.write(f'   • {user.email} ({user.get_user_type_display()})')

# Usage: python manage.py test_password_reset --email=test@ntech.com
