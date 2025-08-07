from django.core.management.base import BaseCommand
from exams.models import Subject, Question, Exam
from django.utils import timezone
from authentication.models import CustomUser


class Command(BaseCommand):
    help = 'Create Geopolitics exam with 20 questions'

    def handle(self, *args, **options):
        # Get or create an admin user for created_by field
        admin_user = CustomUser.objects.filter(is_admin=True).first()
        if not admin_user:
            admin_user = CustomUser.objects.filter(is_superuser=True).first()
        
        if not admin_user:
            self.stdout.write(self.style.ERROR("No admin user found. Please create an admin user first."))
            return
        # Create or get Geopolitics subject
        subject, created = Subject.objects.get_or_create(
            name='Geopolitics',
            defaults={'description': 'Study of politics, especially international relations, as influenced by geography'}
        )
        
        if created:
            self.stdout.write(f"✓ Created subject: {subject.name}")
        else:
            self.stdout.write(f"✓ Subject already exists: {subject.name}")

        # Geopolitics questions data
        questions_data = [
            {
                'text': 'Which of the following best describes the concept of "geopolitics"?',
                'option_a': 'The study of political systems within individual countries',
                'option_b': 'The influence of geography on politics and international relations',
                'option_c': 'The economic relationships between neighboring countries',
                'option_d': 'The study of population distribution and demographics',
                'correct_answer': 'B'
            },
            {
                'text': 'The Heartland Theory was proposed by which geopolitical theorist?',
                'option_a': 'Alfred Thayer Mahan',
                'option_b': 'Nicholas Spykman',
                'option_c': 'Halford Mackinder',
                'option_d': 'Karl Haushofer',
                'correct_answer': 'C'
            },
            {
                'text': 'According to Mackinder\'s Heartland Theory, who controls the Heartland controls:',
                'option_a': 'The seas',
                'option_b': 'The World-Island',
                'option_c': 'The Americas',
                'option_d': 'The Pacific Ocean',
                'correct_answer': 'B'
            },
            {
                'text': 'Which geographic region is considered the "Rimland" in Spykman\'s theory?',
                'option_a': 'Central Asia and Eastern Europe',
                'option_b': 'The coastal areas surrounding the Heartland',
                'option_c': 'The Americas',
                'option_d': 'Sub-Saharan Africa',
                'correct_answer': 'B'
            },
            {
                'text': 'The Suez Canal is strategically important because it:',
                'option_a': 'Connects the Mediterranean and Red Seas',
                'option_b': 'Provides freshwater to North Africa',
                'option_c': 'Contains significant oil reserves',
                'option_d': 'Separates Africa from Asia',
                'correct_answer': 'A'
            },
            {
                'text': 'Which strait controls access between Europe and Asia and has been historically contested?',
                'option_a': 'Strait of Gibraltar',
                'option_b': 'Strait of Hormuz',
                'option_c': 'Bosphorus Strait',
                'option_d': 'Strait of Malacca',
                'correct_answer': 'C'
            },
            {
                'text': 'The "Great Game" historically referred to rivalry between which two powers?',
                'option_a': 'USA and USSR',
                'option_b': 'Britain and Russia',
                'option_c': 'France and Germany',
                'option_d': 'China and Japan',
                'correct_answer': 'B'
            },
            {
                'text': 'Which concept describes a state\'s area of political and economic influence?',
                'option_a': 'Sphere of influence',
                'option_b': 'Buffer zone',
                'option_c': 'Frontier region',
                'option_d': 'Core area',
                'correct_answer': 'A'
            },
            {
                'text': 'The term "Balkanization" refers to:',
                'option_a': 'Economic integration of small states',
                'option_b': 'The fragmentation of a region into smaller, hostile states',
                'option_c': 'Military alliance formation',
                'option_d': 'Cultural homogenization',
                'correct_answer': 'B'
            },
            {
                'text': 'Which body of water is most crucial for global oil transportation?',
                'option_a': 'Mediterranean Sea',
                'option_b': 'Persian Gulf',
                'option_c': 'North Sea',
                'option_d': 'Caribbean Sea',
                'correct_answer': 'B'
            },
            {
                'text': 'The concept of "Lebensraum" was associated with which country\'s geopolitical thinking?',
                'option_a': 'Soviet Union',
                'option_b': 'Japan',
                'option_c': 'Germany',
                'option_d': 'Italy',
                'correct_answer': 'C'
            },
            {
                'text': 'Which geographic feature has historically served as a natural barrier between Europe and Asia?',
                'option_a': 'Himalayan Mountains',
                'option_b': 'Ural Mountains',
                'option_c': 'Caucasus Mountains',
                'option_d': 'Alps Mountains',
                'correct_answer': 'B'
            },
            {
                'text': 'The "Pivot Area" in Mackinder\'s theory roughly corresponds to which modern region?',
                'option_a': 'Western Europe',
                'option_b': 'Central Asia and parts of Eastern Europe',
                'option_c': 'Southeast Asia',
                'option_d': 'The Middle East',
                'correct_answer': 'B'
            },
            {
                'text': 'Which doctrine stated that the US would prevent further European colonization in the Americas?',
                'option_a': 'Truman Doctrine',
                'option_b': 'Monroe Doctrine',
                'option_c': 'Eisenhower Doctrine',
                'option_d': 'Nixon Doctrine',
                'correct_answer': 'B'
            },
            {
                'text': 'The "Silk Road" historically connected which two major regions?',
                'option_a': 'Europe and Africa',
                'option_b': 'Asia and Europe',
                'option_c': 'Americas and Asia',
                'option_d': 'Africa and Asia',
                'correct_answer': 'B'
            },
            {
                'text': 'Which island nation controls the Strait of Malacca along with Malaysia and Indonesia?',
                'option_a': 'Philippines',
                'option_b': 'Singapore',
                'option_c': 'Brunei',
                'option_d': 'East Timor',
                'correct_answer': 'B'
            },
            {
                'text': 'The geopolitical importance of Afghanistan stems primarily from its:',
                'option_a': 'Oil reserves',
                'option_b': 'Strategic location between major powers',
                'option_c': 'Naval capabilities',
                'option_d': 'Industrial capacity',
                'correct_answer': 'B'
            },
            {
                'text': 'Which theory emphasizes the importance of sea power in global dominance?',
                'option_a': 'Heartland Theory',
                'option_b': 'Rimland Theory',
                'option_c': 'Sea Power Theory',
                'option_d': 'Air Power Theory',
                'correct_answer': 'C'
            },
            {
                'text': 'The "demographic transition" model is most relevant to geopolitics because it affects:',
                'option_a': 'Military recruitment potential',
                'option_b': 'Economic development patterns',
                'option_c': 'Resource consumption',
                'option_d': 'All of the above',
                'correct_answer': 'D'
            },
            {
                'text': 'Which modern concept describes the interconnectedness of global political and economic systems?',
                'option_a': 'Multipolarity',
                'option_b': 'Globalization',
                'option_c': 'Regionalism',
                'option_d': 'Isolationism',
                'correct_answer': 'B'
            }
        ]

        # Create questions
        created_questions = []
        for i, q_data in enumerate(questions_data, 1):
            question, created = Question.objects.get_or_create(
                subject=subject,
                question_text=q_data['text'],
                defaults={
                    'option_a': q_data['option_a'],
                    'option_b': q_data['option_b'],
                    'option_c': q_data['option_c'],
                    'option_d': q_data['option_d'],
                    'correct_answer': q_data['correct_answer'],
                    'marks': 1,
                    'difficulty': 'medium',
                    'created_by': admin_user
                }
            )
            
            if created:
                created_questions.append(question)
                self.stdout.write(f"✓ Created question {i}: {q_data['text'][:50]}...")
            else:
                self.stdout.write(f"⚠ Question {i} already exists: {q_data['text'][:50]}...")

        # Create Geopolitics exam
        exam, created = Exam.objects.get_or_create(
            title='Geopolitics Fundamentals Exam',
            subject=subject,
            defaults={
                'description': 'Comprehensive exam covering fundamental concepts in geopolitics, including major theories, strategic locations, and historical developments.',
                'duration_minutes': 30,  # 30 minutes
                'total_marks': 20,  # 20 questions, 1 mark each
                'is_active': True,
                'created_by': admin_user,
            }
        )

        if created:
            # Add all questions to the exam
            all_questions = Question.objects.filter(subject=subject)
            exam.questions.set(all_questions)
            
            self.stdout.write(self.style.SUCCESS(f"\n✅ Successfully created Geopolitics exam!"))
            self.stdout.write(f"📚 Subject: {subject.name}")
            self.stdout.write(f"📝 Exam: {exam.title}")
            self.stdout.write(f"❓ Questions: {exam.questions.count()}")
            self.stdout.write(f"⏱️ Duration: {exam.duration_minutes} minutes")
            self.stdout.write(f"🎯 Total Marks: {exam.total_marks}")
            self.stdout.write(f"📈 Status: {'Active' if exam.is_active else 'Inactive'}")
            
        else:
            self.stdout.write(self.style.WARNING(f"⚠ Exam already exists: {exam.title}"))

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Geopolitics exam setup completed!"))
        self.stdout.write(f"🔗 Students can now access this exam from the dashboard.")
        self.stdout.write(f"⚙️ Admins can modify questions at /admin/exams/question/")
