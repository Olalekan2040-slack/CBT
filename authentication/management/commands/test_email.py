from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test email configuration by sending a test email'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            help='Email address to send test email to',
            default='olalekanquadri58@gmail.com'
        )
    
    def handle(self, *args, **options):
        recipient = options['to']
        
        self.stdout.write('📧 Testing email configuration...')
        self.stdout.write(f'   Sending to: {recipient}')
        self.stdout.write(f'   From: {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'   SMTP Host: {settings.EMAIL_HOST}')
        
        try:
            send_mail(
                subject='🚀 N-TECH CBT System - Email Test',
                message='''
Hello!

This is a test email from your N-TECH CBT System to verify that email configuration is working correctly.

✅ SMTP Configuration: Working
✅ Authentication: Successful  
✅ Email Delivery: Confirmed

Your N-TECH CBT system is now ready to send:
- Password reset emails
- Email verification messages
- User notifications
- System alerts

Best regards,
N-TECH CBT System
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Test email sent successfully to {recipient}!'
                )
            )
            self.stdout.write('📬 Check your inbox for the test email.')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Failed to send email: {str(e)}'
                )
            )
            self.stdout.write('🔧 Please check your email configuration.')
            
            # Show current email settings (without password)
            self.stdout.write('\n📋 Current Email Settings:')
            self.stdout.write(f'   Backend: {settings.EMAIL_BACKEND}')
            self.stdout.write(f'   Host: {settings.EMAIL_HOST}')
            self.stdout.write(f'   Port: {settings.EMAIL_PORT}')
            self.stdout.write(f'   TLS: {settings.EMAIL_USE_TLS}')
            self.stdout.write(f'   User: {settings.EMAIL_HOST_USER}')
            self.stdout.write(f'   From: {settings.DEFAULT_FROM_EMAIL}')
