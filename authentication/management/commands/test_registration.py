from django.core.management.base import BaseCommand
from authentication.models import CustomUser, CourseEnrollment
from exams.models import Course

class Command(BaseCommand):
    help = 'Test registration flow and course enrollment'

    def handle(self, *args, **options):
        # Test student registration
        self.stdout.write(self.style.SUCCESS('Testing N-TECH registration flow...'))
        
        # Check if courses exist
        courses = Course.objects.filter(is_active=True)
        self.stdout.write(f'Available courses: {courses.count()}')
        for course in courses:
            self.stdout.write(f'  - {course.code}: {course.name}')
        
        # Test creating a student
        if not CustomUser.objects.filter(email='test@ntech.com').exists():
            try:
                # Get a course to enroll in
                react_course = Course.objects.filter(code='frontend_react').first()
                
                if react_course:
                    # Create test student
                    test_student = CustomUser.objects.create_user(
                        username='test_student',
                        email='test@ntech.com',
                        first_name='Test',
                        last_name='Student',
                        user_type='student',
                        is_approved=True
                    )
                    
                    # Enroll in React course
                    enrollment = CourseEnrollment.objects.create(
                        student=test_student,
                        course=react_course,
                        is_active=True
                    )
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully created test student: {test_student.email}\n'
                            f'Enrolled in: {react_course.name}\n'
                            f'Enrollment ID: {enrollment.id}'
                        )
                    )
                else:
                    self.stdout.write(self.style.ERROR('No React course found!'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating test student: {e}'))
        else:
            self.stdout.write('Test student already exists')
            
        # Check enrollments
        enrollments = CourseEnrollment.objects.all()
        self.stdout.write(f'\nTotal enrollments: {enrollments.count()}')
        for enrollment in enrollments:
            self.stdout.write(f'  - {enrollment.student.email} -> {enrollment.course.name}')
