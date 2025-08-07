from django.core.management.base import BaseCommand
from authentication.models import CustomUser


class Command(BaseCommand):
    help = 'Update existing users to new user type system'

    def handle(self, *args, **options):
        # Update admin user
        admin_users = CustomUser.objects.filter(is_superuser=True)
        for user in admin_users:
            user.user_type = 'admin'
            user.is_approved = True
            user.save()
            self.stdout.write(f"✓ Updated {user.email} to admin type")
        
        # Update users who don't have user_type set
        users_without_type = CustomUser.objects.filter(user_type='student', is_superuser=False)
        for user in users_without_type:
            user.user_type = 'student'
            user.is_approved = True
            user.save()
            self.stdout.write(f"✓ Updated {user.email} to student type")
        
        self.stdout.write(self.style.SUCCESS("✅ User migration completed!"))
        
        # Display current user counts
        total_users = CustomUser.objects.count()
        students = CustomUser.objects.filter(user_type='student').count()
        instructors = CustomUser.objects.filter(user_type='instructor').count()
        approved_instructors = CustomUser.objects.filter(user_type='instructor', is_approved=True).count()
        admins = CustomUser.objects.filter(user_type='admin').count()
        superusers = CustomUser.objects.filter(is_superuser=True).count()
        
        self.stdout.write(f"\n📊 Current User Statistics:")
        self.stdout.write(f"👥 Total Users: {total_users}")
        self.stdout.write(f"👨‍🎓 Students: {students}")
        self.stdout.write(f"👨‍🏫 Instructors: {instructors} ({approved_instructors} approved)")
        self.stdout.write(f"👨‍💼 Admins: {admins}")
        self.stdout.write(f"🔑 Superusers: {superusers}")
