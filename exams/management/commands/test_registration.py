from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from exams.models import Course
from authentication.models import CourseEnrollment
from authentication.forms import StudentRegistrationForm

User = get_user_model()

class Command(BaseCommand):
    help = 'Test student registration form'

    def handle(self, *args, **options):
        self.stdout.write('🧪 Testing Student Registration Form...')
        
        # Test form with sample data
        form_data = {
            'username': 'testuser123',
            'email': 'testuser123@ntech.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890',
            'password1': 'testpass123!',
            'password2': 'testpass123!',
            'course': Course.objects.first().pk if Course.objects.exists() else None
        }
        
        # Check if courses exist
        courses = Course.objects.all()
        self.stdout.write(f'📚 Available Courses: {courses.count()}')
        for course in courses:
            self.stdout.write(f'  • {course.pk}: {course.name}')
        
        if not courses.exists():
            self.stdout.write(self.style.ERROR('❌ No courses found! Run setup_ntech first.'))
            return
        
        # Create form instance
        form = StudentRegistrationForm(data=form_data)
        
        # Check form validity
        if form.is_valid():
            self.stdout.write(self.style.SUCCESS('✅ Form is valid'))
            try:
                # Don't actually save, just test
                self.stdout.write('📝 Form data looks good for registration')
                self.stdout.write(f'  • Username: {form.cleaned_data["username"]}')
                self.stdout.write(f'  • Email: {form.cleaned_data["email"]}')
                self.stdout.write(f'  • Course: {form.cleaned_data["course"]}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Form save would fail: {e}'))
        else:
            self.stdout.write(self.style.ERROR('❌ Form is invalid'))
            for field, errors in form.errors.items():
                self.stdout.write(f'  • {field}: {errors}')
        
        # Check existing registrations
        students = User.objects.filter(user_type='student')
        self.stdout.write(f'👥 Existing Students: {students.count()}')
        
        enrollments = CourseEnrollment.objects.all()
        self.stdout.write(f'📝 Existing Enrollments: {enrollments.count()}')
