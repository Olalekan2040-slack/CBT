from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from exams.models import Subject, Question, Exam, ExamQuestion

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Create admin user
        if not User.objects.filter(email='admin@cbt.com').exists():
            admin = User.objects.create_user(
                username='admin',
                email='admin@cbt.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                is_admin=True,
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(f'Created admin user: {admin.email}')
        
        # Create student user
        if not User.objects.filter(email='student@cbt.com').exists():
            student = User.objects.create_user(
                username='student',
                email='student@cbt.com',
                password='student123',
                first_name='John',
                last_name='Doe',
                is_student=True
            )
            self.stdout.write(f'Created student user: {student.email}')
        
        # Create subjects
        subjects_data = [
            {'name': 'Mathematics', 'description': 'Basic and advanced mathematics topics'},
            {'name': 'English Language', 'description': 'Grammar, comprehension, and vocabulary'},
            {'name': 'Computer Science', 'description': 'Programming, algorithms, and computer systems'},
            {'name': 'Physics', 'description': 'Classical and modern physics concepts'},
            {'name': 'Biology', 'description': 'Life sciences and biological processes'},
        ]
        
        subjects = []
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                name=subject_data['name'],
                defaults={'description': subject_data['description']}
            )
            subjects.append(subject)
            if created:
                self.stdout.write(f'Created subject: {subject.name}')
        
        # Create sample questions for Mathematics
        math_subject = subjects[0]
        admin_user = User.objects.get(email='admin@cbt.com')
        
        questions_data = [
            {
                'question_text': 'What is 2 + 2?',
                'option_a': '3',
                'option_b': '4',
                'option_c': '5',
                'option_d': '6',
                'correct_answer': 'B',
                'marks': 1,
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is the square root of 16?',
                'option_a': '2',
                'option_b': '3',
                'option_c': '4',
                'option_d': '5',
                'correct_answer': 'C',
                'marks': 1,
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is 15 × 7?',
                'option_a': '105',
                'option_b': '95',
                'option_c': '115',
                'option_d': '85',
                'correct_answer': 'A',
                'marks': 2,
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is the value of π (pi) approximately?',
                'option_a': '3.14159',
                'option_b': '2.71828',
                'option_c': '1.41421',
                'option_d': '2.23606',
                'correct_answer': 'A',
                'marks': 1,
                'difficulty': 'easy'
            },
            {
                'question_text': 'If x = 5, what is 3x + 7?',
                'option_a': '20',
                'option_b': '22',
                'option_c': '25',
                'option_d': '27',
                'correct_answer': 'B',
                'marks': 2,
                'difficulty': 'medium'
            }
        ]
        
        questions = []
        for q_data in questions_data:
            question, created = Question.objects.get_or_create(
                question_text=q_data['question_text'],
                subject=math_subject,
                defaults={
                    'option_a': q_data['option_a'],
                    'option_b': q_data['option_b'],
                    'option_c': q_data['option_c'],
                    'option_d': q_data['option_d'],
                    'correct_answer': q_data['correct_answer'],
                    'marks': q_data['marks'],
                    'difficulty': q_data['difficulty'],
                    'created_by': admin_user
                }
            )
            questions.append(question)
            if created:
                self.stdout.write(f'Created question: {question.question_text[:50]}...')
        
        # Create Computer Science questions
        cs_subject = subjects[2]
        cs_questions_data = [
            {
                'question_text': 'What does HTML stand for?',
                'option_a': 'Hypertext Markup Language',
                'option_b': 'High-level Text Management Language',
                'option_c': 'Home Tool Markup Language',
                'option_d': 'Hyperlink and Text Markup Language',
                'correct_answer': 'A',
                'marks': 1,
                'difficulty': 'easy'
            },
            {
                'question_text': 'Which programming language is known as the "mother of all languages"?',
                'option_a': 'Python',
                'option_b': 'Java',
                'option_c': 'C',
                'option_d': 'Assembly',
                'correct_answer': 'C',
                'marks': 2,
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is the time complexity of binary search?',
                'option_a': 'O(n)',
                'option_b': 'O(log n)',
                'option_c': 'O(n²)',
                'option_d': 'O(1)',
                'correct_answer': 'B',
                'marks': 3,
                'difficulty': 'hard'
            }
        ]
        
        cs_questions = []
        for q_data in cs_questions_data:
            question, created = Question.objects.get_or_create(
                question_text=q_data['question_text'],
                subject=cs_subject,
                defaults={
                    'option_a': q_data['option_a'],
                    'option_b': q_data['option_b'],
                    'option_c': q_data['option_c'],
                    'option_d': q_data['option_d'],
                    'correct_answer': q_data['correct_answer'],
                    'marks': q_data['marks'],
                    'difficulty': q_data['difficulty'],
                    'created_by': admin_user
                }
            )
            cs_questions.append(question)
            if created:
                self.stdout.write(f'Created CS question: {question.question_text[:50]}...')
        
        # Create sample exams
        exams_data = [
            {
                'title': 'Basic Mathematics Test',
                'description': 'A test covering basic mathematical concepts',
                'subject': math_subject,
                'duration_minutes': 30,
                'questions': questions[:3]
            },
            {
                'title': 'Advanced Mathematics Exam',
                'description': 'Advanced mathematical problems and concepts',
                'subject': math_subject,
                'duration_minutes': 60,
                'questions': questions
            },
            {
                'title': 'Computer Science Fundamentals',
                'description': 'Basic computer science concepts and programming',
                'subject': cs_subject,
                'duration_minutes': 45,
                'questions': cs_questions
            }
        ]
        
        for exam_data in exams_data:
            exam, created = Exam.objects.get_or_create(
                title=exam_data['title'],
                defaults={
                    'description': exam_data['description'],
                    'subject': exam_data['subject'],
                    'duration_minutes': exam_data['duration_minutes'],
                    'total_marks': sum(q.marks for q in exam_data['questions']),
                    'is_active': True,
                    'randomize_questions': True,
                    'created_by': admin_user
                }
            )
            
            if created:
                # Add questions to exam
                for i, question in enumerate(exam_data['questions']):
                    ExamQuestion.objects.create(
                        exam=exam,
                        question=question,
                        order=i + 1
                    )
                self.stdout.write(f'Created exam: {exam.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write('Admin login: admin@cbt.com / admin123')
        self.stdout.write('Student login: student@cbt.com / student123')
