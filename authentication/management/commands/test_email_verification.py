from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import uuid

User = get_user_model()

class Command(BaseCommand):
    help = 'Test email verification URL generation'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to test verification for',
        )
    
    def handle(self, *args, **options):
        email = options.get('email')
        
        if not email:
            self.stdout.write("Testing email verification URL generation...")
            
            # Create a test user
            test_user = User(
                username='testuser',
                email='test@example.com',
                first_name='Test',
                last_name='User',
                email_verification_token=uuid.uuid4()
            )
            
            uid = urlsafe_base64_encode(force_bytes(123))  # Test user ID
            token = str(test_user.email_verification_token)
            
            try:
                url = reverse('authentication:verify_email', kwargs={'uid': uid, 'token': token})
                self.stdout.write(f"✅ URL Pattern Working!")
                self.stdout.write(f"   Generated URL: {url}")
                self.stdout.write(f"   UID: {uid}")
                self.stdout.write(f"   Token: {token}")
            except Exception as e:
                self.stdout.write(f"❌ URL Generation Failed: {str(e)}")
        
        else:
            try:
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = str(user.email_verification_token)
                
                url = reverse('authentication:verify_email', kwargs={'uid': uid, 'token': token})
                full_url = f"http://127.0.0.1:8000{url}"
                
                self.stdout.write(f"✅ Verification URL for {email}:")
                self.stdout.write(f"   {full_url}")
                self.stdout.write(f"   UID: {uid}")
                self.stdout.write(f"   Token: {token}")
                
            except User.DoesNotExist:
                self.stdout.write(f"❌ User with email {email} not found")
            except Exception as e:
                self.stdout.write(f"❌ Error: {str(e)}")
