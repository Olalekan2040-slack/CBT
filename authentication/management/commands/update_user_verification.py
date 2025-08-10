from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Command(BaseCommand):
    help = 'Update existing users with email verification fields'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--verify-all',
            action='store_true',
            help='Mark all existing users as email verified',
        )
    
    def handle(self, *args, **options):
        users = User.objects.all()
        updated_count = 0
        
        for user in users:
            needs_update = False
            
            # Add email verification token if missing
            if not user.email_verification_token:
                user.email_verification_token = uuid.uuid4()
                needs_update = True
            
            # If verify-all flag is set, mark all users as verified
            if options['verify_all'] and not user.is_email_verified:
                user.is_email_verified = True
                needs_update = True
                self.stdout.write(f"Marked {user.email} as email verified")
            
            if needs_update:
                user.save()
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} users'
            )
        )
        
        # Show summary
        total_users = User.objects.count()
        verified_users = User.objects.filter(is_email_verified=True).count()
        unverified_users = total_users - verified_users
        
        self.stdout.write(f"\nUser Summary:")
        self.stdout.write(f"Total users: {total_users}")
        self.stdout.write(f"Email verified: {verified_users}")
        self.stdout.write(f"Unverified: {unverified_users}")
