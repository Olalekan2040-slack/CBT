from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from exams.models import Course, Subject, Question, Exam
from authentication.models import CourseEnrollment

User = get_user_model()

class Command(BaseCommand):
    help = 'Debug CBT system state'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== N-TECH CBT DEBUG REPORT ==='))
        
        # Check courses
        courses = Course.objects.all()
        self.stdout.write(f'📚 Total Courses: {courses.count()}')
        for course in courses:
            self.stdout.write(f'  • {course.name} ({course.code})')
        
        # Check subjects
        subjects = Subject.objects.all()
        self.stdout.write(f'📖 Total Subjects: {subjects.count()}')
        
        # Check questions
        questions = Question.objects.all()
        self.stdout.write(f'❓ Total Questions: {questions.count()}')
        for question in questions[:3]:  # Show first 3
            self.stdout.write(f'  • {question.course.name if question.course else "No Course"} - {question.question_text[:50]}...')
        
        # Check exams
        exams = Exam.objects.all()
        self.stdout.write(f'📋 Total Exams: {exams.count()}')
        for exam in exams:
            question_count = exam.questions.count()
            self.stdout.write(f'  • {exam.title} - Course: {exam.course.name if exam.course else "None"} - Questions: {question_count} - Active: {exam.is_active}')
        
        # Check users
        students = User.objects.filter(user_type='student')
        self.stdout.write(f'👥 Total Students: {students.count()}')
        
        # Check enrollments
        enrollments = CourseEnrollment.objects.all()
        self.stdout.write(f'📝 Total Enrollments: {enrollments.count()}')
        for enrollment in enrollments:
            self.stdout.write(f'  • {enrollment.student.email} enrolled in {enrollment.course.name} - Active: {enrollment.is_active}')
        
        # Check student exam access
        if students.exists():
            student = students.first()
            self.stdout.write(f'\n🔍 DEBUG: Student {student.email}')
            
            # Get student enrollments
            student_enrollments = CourseEnrollment.objects.filter(student=student, is_active=True)
            self.stdout.write(f'  • Active Enrollments: {student_enrollments.count()}')
            
            for enrollment in student_enrollments:
                course = enrollment.course
                self.stdout.write(f'  • Enrolled in: {course.name}')
                
                # Check exams for this course
                course_exams = Exam.objects.filter(course=course, is_active=True)
                self.stdout.write(f'  • Available Exams for {course.name}: {course_exams.count()}')
                
                for exam in course_exams:
                    question_count = exam.questions.count()
                    self.stdout.write(f'    - {exam.title}: {question_count} questions')
        
        self.stdout.write(self.style.SUCCESS('\n=== END DEBUG REPORT ==='))
