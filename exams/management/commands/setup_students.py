from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from exams.models import Course
from authentication.models import CourseEnrollment

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test student accounts'

    def handle(self, *args, **options):
        # Create/update test@ntech.com
        try:
            student = User.objects.get(email='test@ntech.com')
            student.set_password('testpass123')
            student.save()
            self.stdout.write(f'✅ Updated password for {student.email}')
        except User.DoesNotExist:
            # Create new student
            react_course = Course.objects.get(code='frontend_react')
            student = User.objects.create_user(
                email='test@ntech.com',
                password='testpass123',
                first_name='Test',
                last_name='Student',
                user_type='student'
            )
            # Enroll in React course
            CourseEnrollment.objects.create(
                student=student,
                course=react_course,
                is_active=True
            )
            self.stdout.write(f'✅ Created student {student.email}')

        # Create/update student@cbt.com  
        try:
            student2 = User.objects.get(email='student@cbt.com')
            self.stdout.write(f'✅ Found existing student {student2.email}')
        except User.DoesNotExist:
            # Create new student
            react_course = Course.objects.get(code='frontend_react')
            student2 = User.objects.create_user(
                email='student@cbt.com',
                password='testpass123',
                first_name='CBT',
                last_name='Student',
                user_type='student'
            )
            self.stdout.write(f'✅ Created student {student2.email}')

        # Enroll student@cbt.com in React course
        react_course = Course.objects.get(code='frontend_react')
        enrollment, created = CourseEnrollment.objects.get_or_create(
            student=User.objects.get(email='student@cbt.com'),
            course=react_course,
            defaults={'is_active': True}
        )
        if created:
            self.stdout.write(f'✅ Enrolled student@cbt.com in {react_course.name}')
        else:
            enrollment.is_active = True
            enrollment.save()
            self.stdout.write(f'✅ Updated enrollment for student@cbt.com')

        self.stdout.write(self.style.SUCCESS('\n=== STUDENT ACCOUNTS READY ==='))
        self.stdout.write('📧 test@ntech.com - Password: testpass123')
        self.stdout.write('📧 student@cbt.com - Password: testpass123')
        self.stdout.write('🎓 Both enrolled in: Frontend Development with React.js')
