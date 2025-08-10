from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from exams.models import Course
from authentication.models import CourseEnrollment

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a test student to verify registration works'

    def handle(self, *args, **options):
        # Get a course
        course = Course.objects.filter(code='frontend_react').first()
        if not course:
            self.stdout.write(self.style.ERROR('❌ No React course found'))
            return
        
        # Create test student
        test_email = 'newstudent@test.com'
        
        # Delete if exists
        User.objects.filter(email=test_email).delete()
        
        try:
            # Create student
            student = User.objects.create_user(
                username='newstudent',
                email=test_email,
                password='testpass123',
                first_name='New',
                last_name='Student',
                user_type='student',
                is_approved=True
            )
            
            # Enroll in course
            enrollment = CourseEnrollment.objects.create(
                student=student,
                course=course,
                is_active=True
            )
            
            self.stdout.write(self.style.SUCCESS(f'✅ Created student: {student.email}'))
            self.stdout.write(self.style.SUCCESS(f'✅ Enrolled in: {course.name}'))
            self.stdout.write(f'🔑 Login credentials:')
            self.stdout.write(f'   Email: {test_email}')
            self.stdout.write(f'   Password: testpass123')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {e}'))
