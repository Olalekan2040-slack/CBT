from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from exams.models import Course, Subject, Question, Exam
from authentication.models import CourseEnrollment
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Setup N-TECH CBT system with courses and sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up N-TECH CBT System...'))
        
        with transaction.atomic():
            # Create N-TECH courses
            courses_data = [
                {
                    'code': 'fullstack',
                    'name': 'Full Stack Web Development',
                    'description': 'Complete full-stack web development training covering frontend and backend technologies',
                    'duration_weeks': 16
                },
                {
                    'code': 'frontend_react',
                    'name': 'Frontend Development with React.js',
                    'description': 'Modern frontend development using React.js, HTML5, CSS3, and JavaScript',
                    'duration_weeks': 12
                },
                {
                    'code': 'backend_django',
                    'name': 'Backend Development with Python Django',
                    'description': 'Server-side development using Python Django framework',
                    'duration_weeks': 12
                },
                {
                    'code': 'backend_fastapi',
                    'name': 'Backend Development with FastAPI',
                    'description': 'Modern API development using FastAPI and Python',
                    'duration_weeks': 10
                },
                {
                    'code': 'data_analysis',
                    'name': 'Data Analysis',
                    'description': 'Data analysis and visualization using Python, Pandas, and analytics tools',
                    'duration_weeks': 14
                },
                {
                    'code': 'data_science',
                    'name': 'Data Science',
                    'description': 'Machine learning, data science, and AI using Python',
                    'duration_weeks': 16
                },
                {
                    'code': 'cybersecurity',
                    'name': 'Cybersecurity',
                    'description': 'Network security, ethical hacking, and cybersecurity fundamentals',
                    'duration_weeks': 14
                },
                {
                    'code': 'ui_ux',
                    'name': 'UI/UX Design',
                    'description': 'User interface and user experience design principles and tools',
                    'duration_weeks': 12
                },
                {
                    'code': 'mobile_dev',
                    'name': 'Mobile Development',
                    'description': 'Mobile app development for iOS and Android platforms',
                    'duration_weeks': 14
                }
            ]
            
            courses_created = 0
            for course_data in courses_data:
                course, created = Course.objects.get_or_create(
                    code=course_data['code'],
                    defaults=course_data
                )
                if created:
                    courses_created += 1
                    self.stdout.write(f'Created course: {course.name}')
            
            self.stdout.write(f'Total courses created: {courses_created}')
            
            # Create subjects for each course
            subjects_data = {
                'fullstack': ['HTML/CSS Fundamentals', 'JavaScript Programming', 'Frontend Frameworks', 'Backend Development', 'Database Design', 'API Development'],
                'frontend_react': ['HTML/CSS Mastery', 'JavaScript ES6+', 'React Fundamentals', 'State Management', 'React Router', 'Testing'],
                'backend_django': ['Python Fundamentals', 'Django Basics', 'Models and ORM', 'Views and Templates', 'REST APIs', 'Deployment'],
                'backend_fastapi': ['Python Advanced', 'FastAPI Basics', 'API Design', 'Authentication', 'Database Integration', 'Testing'],
                'data_analysis': ['Python for Data', 'Pandas Library', 'Data Visualization', 'Statistical Analysis', 'Excel Integration', 'Reporting'],
                'data_science': ['Python Programming', 'Machine Learning', 'Data Mining', 'Neural Networks', 'Deep Learning', 'AI Applications'],
                'cybersecurity': ['Network Security', 'Ethical Hacking', 'Cryptography', 'Security Protocols', 'Incident Response', 'Compliance'],
                'ui_ux': ['Design Principles', 'User Research', 'Wireframing', 'Prototyping', 'Design Tools', 'Usability Testing'],
                'mobile_dev': ['Mobile UI/UX', 'React Native', 'Flutter', 'Native Development', 'App Store Publishing', 'Performance Optimization']
            }
            
            subjects_created = 0
            for course in Course.objects.all():
                if course.code in subjects_data:
                    for subject_name in subjects_data[course.code]:
                        subject, created = Subject.objects.get_or_create(
                            course=course,
                            name=subject_name,
                            defaults={
                                'description': f'{subject_name} module for {course.name}'
                            }
                        )
                        if created:
                            subjects_created += 1
            
            self.stdout.write(f'Total subjects created: {subjects_created}')
            
            # Create sample questions for React.js course
            react_course = Course.objects.get(code='frontend_react')
            react_fundamentals = Subject.objects.get(course=react_course, name='React Fundamentals')
            
            # Get admin user
            admin_user = User.objects.filter(user_type='admin').first()
            if not admin_user:
                admin_user = User.objects.filter(is_superuser=True).first()
            
            if admin_user:
                sample_questions = [
                    {
                        'question_text': 'What is React?',
                        'option_a': 'A database management system',
                        'option_b': 'A JavaScript library for building user interfaces',
                        'option_c': 'A server-side programming language',
                        'option_d': 'A CSS framework',
                        'correct_answer': 'B',
                        'difficulty': 'easy'
                    },
                    {
                        'question_text': 'What is JSX in React?',
                        'option_a': 'A database query language',
                        'option_b': 'A CSS preprocessor',
                        'option_c': 'A syntax extension that allows writing HTML-like code in JavaScript',
                        'option_d': 'A testing framework',
                        'correct_answer': 'C',
                        'difficulty': 'easy'
                    },
                    {
                        'question_text': 'Which method is used to render a React component?',
                        'option_a': 'ReactDOM.render()',
                        'option_b': 'React.render()',
                        'option_c': 'render()',
                        'option_d': 'component.render()',
                        'correct_answer': 'A',
                        'difficulty': 'medium'
                    },
                    {
                        'question_text': 'What are React hooks?',
                        'option_a': 'Functions that let you use state and lifecycle features in functional components',
                        'option_b': 'CSS styling methods',
                        'option_c': 'Database connection methods',
                        'option_d': 'Server-side rendering techniques',
                        'correct_answer': 'A',
                        'difficulty': 'medium'
                    },
                    {
                        'question_text': 'Which hook is used to manage state in functional components?',
                        'option_a': 'useEffect',
                        'option_b': 'useState',
                        'option_c': 'useContext',
                        'option_d': 'useReducer',
                        'correct_answer': 'B',
                        'difficulty': 'easy'
                    },
                    {
                        'question_text': 'What is the virtual DOM?',
                        'option_a': 'A physical representation of the DOM',
                        'option_b': 'A JavaScript representation of the real DOM kept in memory',
                        'option_c': 'A CSS framework',
                        'option_d': 'A database schema',
                        'correct_answer': 'B',
                        'difficulty': 'medium'
                    },
                    {
                        'question_text': 'How do you pass data from parent to child component?',
                        'option_a': 'Using state',
                        'option_b': 'Using props',
                        'option_c': 'Using context',
                        'option_d': 'Using refs',
                        'correct_answer': 'B',
                        'difficulty': 'easy'
                    },
                    {
                        'question_text': 'What is the purpose of useEffect hook?',
                        'option_a': 'To manage component state',
                        'option_b': 'To perform side effects in functional components',
                        'option_c': 'To create components',
                        'option_d': 'To handle events',
                        'correct_answer': 'B',
                        'difficulty': 'medium'
                    },
                    {
                        'question_text': 'What is prop drilling?',
                        'option_a': 'A method to create holes in components',
                        'option_b': 'Passing props through multiple component layers',
                        'option_c': 'A debugging technique',
                        'option_d': 'A performance optimization',
                        'correct_answer': 'B',
                        'difficulty': 'hard'
                    },
                    {
                        'question_text': 'Which of the following is used for routing in React?',
                        'option_a': 'React Router',
                        'option_b': 'Redux',
                        'option_c': 'Axios',
                        'option_d': 'Material-UI',
                        'correct_answer': 'A',
                        'difficulty': 'easy'
                    }
                ]
                
                questions_created = 0
                for q_data in sample_questions:
                    question, created = Question.objects.get_or_create(
                        subject=react_fundamentals,
                        question_text=q_data['question_text'],
                        defaults={
                            'course': react_course,
                            'option_a': q_data['option_a'],
                            'option_b': q_data['option_b'],
                            'option_c': q_data['option_c'],
                            'option_d': q_data['option_d'],
                            'correct_answer': q_data['correct_answer'],
                            'difficulty': q_data['difficulty'],
                            'marks': 1,
                            'created_by': admin_user
                        }
                    )
                    if created:
                        questions_created += 1
                
                self.stdout.write(f'Created {questions_created} sample questions for React Fundamentals')
                
                # Create a sample exam
                exam, created = Exam.objects.get_or_create(
                    title='React Fundamentals Assessment',
                    course=react_course,
                    subject=react_fundamentals,
                    defaults={
                        'description': 'Assessment covering React.js fundamentals including components, JSX, hooks, and basic concepts.',
                        'duration_minutes': 20,
                        'questions_to_display': 8,
                        'total_marks': 8,
                        'is_active': True,
                        'randomize_questions': True,
                        'show_results_immediately': True,
                        'created_by': admin_user
                    }
                )
                
                if created:
                    # Add questions to exam
                    questions = Question.objects.filter(subject=react_fundamentals)
                    for i, question in enumerate(questions):
                        exam.examquestion_set.create(question=question, order=i)
                    
                    self.stdout.write(f'Created exam: {exam.title}')
            
            self.stdout.write(self.style.SUCCESS('N-TECH CBT system setup completed!'))
            self.stdout.write('Available courses:')
            for course in Course.objects.all():
                self.stdout.write(f'  • {course.name} ({course.code})')
