from django.core.management.base import BaseCommand
from django.urls import reverse
from authentication.models import CustomUser


class Command(BaseCommand):
    help = 'Show admin URLs for question management'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🎯 CBT System Admin Guide"))
        self.stdout.write("=" * 50)
        
        # Check if admin users exist
        admin_users = CustomUser.objects.filter(is_admin=True).count()
        superusers = CustomUser.objects.filter(is_superuser=True).count()
        
        self.stdout.write(f"👨‍💼 Admin Users: {admin_users}")
        self.stdout.write(f"🔑 Superusers: {superusers}")
        self.stdout.write("")
        
        self.stdout.write("🔗 Admin URLs (when server is running on http://127.0.0.1:8000/):")
        self.stdout.write("")
        
        admin_urls = [
            ("🏠 Main Admin Panel", "/admin/"),
            ("❓ Manage Questions", "/admin/exams/question/"),
            ("➕ Add New Question", "/admin/exams/question/add/"),
            ("📝 Manage Exams", "/admin/exams/exam/"),
            ("➕ Create New Exam", "/admin/exams/exam/add/"),
            ("📚 Manage Subjects", "/admin/exams/subject/"),
            ("👥 Manage Users", "/admin/authentication/customuser/"),
            ("📊 View Exam Attempts", "/admin/exams/examattempt/"),
        ]
        
        for name, url in admin_urls:
            self.stdout.write(f"  {name}: http://127.0.0.1:8000{url}")
        
        self.stdout.write("")
        self.stdout.write("📋 Quick Actions:")
        self.stdout.write("  • Login with admin credentials: admin@cbt.com / admin123")
        self.stdout.write("  • Create questions with multiple choice options (A, B, C, D)")
        self.stdout.write("  • Set difficulty level: easy, medium, hard")
        self.stdout.write("  • Assign marks per question (default: 1)")
        self.stdout.write("  • Create exams and assign questions to them")
        self.stdout.write("  • Set exam duration in minutes")
        self.stdout.write("  • Activate/deactivate exams")
        
        self.stdout.write("")
        self.stdout.write("💡 Tips:")
        self.stdout.write("  • Questions can be reused across multiple exams")
        self.stdout.write("  • Use subjects to organize questions by topic")
        self.stdout.write("  • Total exam marks are calculated automatically")
        self.stdout.write("  • Students see randomized question order")
        self.stdout.write("  • Results are emailed automatically after completion")
        
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Happy teaching! 🎓"))
