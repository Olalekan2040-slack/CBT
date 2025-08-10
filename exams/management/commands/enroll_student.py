from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from exams.models import Course
from authentication.models import CourseEnrollment

User = get_user_model()

class Command(BaseCommand):
    help = 'Enroll a student in a course'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Student email')
        parser.add_argument('--course', type=str, help='Course code')

    def handle(self, *args, **options):
        email = options['email']
        course_code = options['course']
        
        if not email or not course_code:
            self.stdout.write(self.style.ERROR('Please provide --email and --course'))
            self.stdout.write('Available courses:')
            for course in Course.objects.all():
                self.stdout.write(f'  • {course.code}: {course.name}')
            return
        
        try:
            student = User.objects.get(email=email, user_type='student')
            course = Course.objects.get(code=course_code)
            
            enrollment, created = CourseEnrollment.objects.get_or_create(
                student=student,
                course=course,
                defaults={'is_active': True}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Enrolled {email} in {course.name}'))
            else:
                enrollment.is_active = True
                enrollment.save()
                self.stdout.write(self.style.SUCCESS(f'✅ Updated enrollment for {email} in {course.name}'))
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Student {email} not found'))
        except Course.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Course {course_code} not found'))

# Usage Examples:
# python manage.py enroll_student --email=student@example.com --course=frontend_react
# python manage.py enroll_student --email=student@example.com --course=backend_django
