from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from exams.models import Subject, Question, Exam
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Create Cybersecurity course with 50 questions'

    def handle(self, *args, **options):
        # Create or get cybersecurity subject
        subject, created = Subject.objects.get_or_create(
            name='Cybersecurity',
            defaults={
                'description': 'Comprehensive cybersecurity course covering network security, encryption, malware, and best practices'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created subject: {subject.name}'))
        else:
            self.stdout.write(f'Subject {subject.name} already exists')

        # Get or create an admin user to be the creator
        try:
            admin_user = User.objects.filter(user_type='admin').first()
            if not admin_user:
                admin_user = User.objects.filter(is_superuser=True).first()
            
            if not admin_user:
                self.stdout.write(self.style.ERROR('No admin user found. Please create an admin user first.'))
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error finding admin user: {e}'))
            return

        # Define 50 cybersecurity questions
        questions_data = [
            # Network Security (15 questions)
            {
                'question_text': 'What is a firewall primarily used for?',
                'option_a': 'To prevent viruses from infecting computers',
                'option_b': 'To block unauthorized access to a network',
                'option_c': 'To encrypt data transmission',
                'option_d': 'To backup important files',
                'correct_answer': 'B',
                'difficulty': 'easy'
            },
            {
                'question_text': 'Which protocol provides secure communication over the internet?',
                'option_a': 'HTTP',
                'option_b': 'FTP',
                'option_c': 'HTTPS',
                'option_d': 'SMTP',
                'correct_answer': 'C',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What does VPN stand for?',
                'option_a': 'Virtual Private Network',
                'option_b': 'Very Personal Network',
                'option_c': 'Virtual Public Network',
                'option_d': 'Verified Private Network',
                'correct_answer': 'A',
                'difficulty': 'easy'
            },
            {
                'question_text': 'Which port is commonly used for HTTPS traffic?',
                'option_a': '80',
                'option_b': '443',
                'option_c': '21',
                'option_d': '25',
                'correct_answer': 'B',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is the primary purpose of intrusion detection systems (IDS)?',
                'option_a': 'To prevent all network attacks',
                'option_b': 'To detect and alert on suspicious network activity',
                'option_c': 'To encrypt network traffic',
                'option_d': 'To backup network configurations',
                'correct_answer': 'B',
                'difficulty': 'medium'
            },
            {
                'question_text': 'Which of the following is a network scanning tool?',
                'option_a': 'Nmap',
                'option_b': 'Photoshop',
                'option_c': 'Microsoft Word',
                'option_d': 'iTunes',
                'correct_answer': 'A',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is a DMZ in network security?',
                'option_a': 'Demilitarized Zone - a buffer network between internal and external networks',
                'option_b': 'Direct Memory Zone',
                'option_c': 'Data Management Zone',
                'option_d': 'Dynamic Memory Zone',
                'correct_answer': 'A',
                'difficulty': 'hard'
            },
            {
                'question_text': 'Which attack involves flooding a network with traffic to make it unavailable?',
                'option_a': 'SQL Injection',
                'option_b': 'Cross-site scripting',
                'option_c': 'Denial of Service (DoS)',
                'option_d': 'Man-in-the-middle',
                'correct_answer': 'C',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is the difference between IDS and IPS?',
                'option_a': 'IDS detects, IPS prevents',
                'option_b': 'IDS prevents, IPS detects',
                'option_c': 'They are the same thing',
                'option_d': 'IDS is hardware, IPS is software',
                'correct_answer': 'A',
                'difficulty': 'hard'
            },
            {
                'question_text': 'Which protocol is used for secure file transfer?',
                'option_a': 'FTP',
                'option_b': 'SFTP',
                'option_c': 'HTTP',
                'option_d': 'SMTP',
                'correct_answer': 'B',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is network segmentation?',
                'option_a': 'Dividing a network into smaller segments for security',
                'option_b': 'Connecting all devices in one segment',
                'option_c': 'Removing network devices',
                'option_d': 'Encrypting network cables',
                'correct_answer': 'A',
                'difficulty': 'medium'
            },
            {
                'question_text': 'Which tool is commonly used for packet analysis?',
                'option_a': 'Wireshark',
                'option_b': 'Notepad',
                'option_c': 'Calculator',
                'option_d': 'Paint',
                'correct_answer': 'A',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is a honeynet?',
                'option_a': 'A network of honeypots designed to attract and analyze attacks',
                'option_b': 'A sweet network protocol',
                'option_c': 'A network for bee farms',
                'option_d': 'A yellow-colored network cable',
                'correct_answer': 'A',
                'difficulty': 'hard'
            },
            {
                'question_text': 'Which type of attack intercepts communication between two parties?',
                'option_a': 'DoS attack',
                'option_b': 'Man-in-the-middle attack',
                'option_c': 'SQL injection',
                'option_d': 'Buffer overflow',
                'correct_answer': 'B',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is the purpose of NAT (Network Address Translation)?',
                'option_a': 'To translate domain names to IP addresses',
                'option_b': 'To map private IP addresses to public IP addresses',
                'option_c': 'To encrypt network traffic',
                'option_d': 'To compress network data',
                'correct_answer': 'B',
                'difficulty': 'medium'
            },

            # Encryption & Cryptography (15 questions)
            {
                'question_text': 'What is the main difference between symmetric and asymmetric encryption?',
                'option_a': 'Symmetric uses one key, asymmetric uses two keys',
                'option_b': 'Symmetric is faster, asymmetric is slower',
                'option_c': 'Symmetric is for data, asymmetric is for passwords',
                'option_d': 'Both A and B are correct',
                'correct_answer': 'D',
                'difficulty': 'medium'
            },
            {
                'question_text': 'Which is an example of symmetric encryption algorithm?',
                'option_a': 'RSA',
                'option_b': 'AES',
                'option_c': 'ECC',
                'option_d': 'Diffie-Hellman',
                'correct_answer': 'B',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What does RSA stand for?',
                'option_a': 'Really Secure Algorithm',
                'option_b': 'Rivest-Shamir-Adleman',
                'option_c': 'Random Security Algorithm',
                'option_d': 'Rapid Security Authentication',
                'correct_answer': 'B',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is a digital signature used for?',
                'option_a': 'Encryption',
                'option_b': 'Authentication and non-repudiation',
                'option_c': 'Data compression',
                'option_d': 'Network routing',
                'correct_answer': 'B',
                'difficulty': 'medium'
            },
            {
                'question_text': 'Which hashing algorithm is considered secure?',
                'option_a': 'MD5',
                'option_b': 'SHA-1',
                'option_c': 'SHA-256',
                'option_d': 'CRC32',
                'correct_answer': 'C',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is the purpose of a salt in password hashing?',
                'option_a': 'To make passwords taste better',
                'option_b': 'To prevent rainbow table attacks',
                'option_c': 'To compress passwords',
                'option_d': 'To encrypt passwords',
                'correct_answer': 'B',
                'difficulty': 'hard'
            },
            {
                'question_text': 'What is PKI?',
                'option_a': 'Public Key Infrastructure',
                'option_b': 'Private Key Interface',
                'option_c': 'Protected Key Installation',
                'option_d': 'Personal Key Identification',
                'correct_answer': 'A',
                'difficulty': 'medium'
            },
            {
                'question_text': 'Which protocol is used for secure email?',
                'option_a': 'SMTP',
                'option_b': 'POP3',
                'option_c': 'S/MIME',
                'option_d': 'IMAP',
                'correct_answer': 'C',
                'difficulty': 'hard'
            },
            {
                'question_text': 'What is the key size of AES-256?',
                'option_a': '128 bits',
                'option_b': '192 bits',
                'option_c': '256 bits',
                'option_d': '512 bits',
                'correct_answer': 'C',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is perfect forward secrecy?',
                'option_a': 'A type of encryption algorithm',
                'option_b': 'Ensuring that session keys are not compromised even if long-term keys are',
                'option_c': 'A method of key distribution',
                'option_d': 'A type of digital signature',
                'correct_answer': 'B',
                'difficulty': 'hard'
            },
            {
                'question_text': 'Which of the following is used for key exchange?',
                'option_a': 'Diffie-Hellman',
                'option_b': 'AES',
                'option_c': 'SHA-256',
                'option_d': 'MD5',
                'correct_answer': 'A',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is the main purpose of a certificate authority (CA)?',
                'option_a': 'To encrypt data',
                'option_b': 'To issue and verify digital certificates',
                'option_c': 'To store passwords',
                'option_d': 'To compress files',
                'correct_answer': 'B',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is steganography?',
                'option_a': 'A type of encryption',
                'option_b': 'Hiding data within other data',
                'option_c': 'A hashing algorithm',
                'option_d': 'A network protocol',
                'correct_answer': 'B',
                'difficulty': 'hard'
            },
            {
                'question_text': 'What is the primary weakness of MD5?',
                'option_a': 'Too slow',
                'option_b': 'Vulnerable to collision attacks',
                'option_c': 'Too complex',
                'option_d': 'Requires too much memory',
                'correct_answer': 'B',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is elliptic curve cryptography (ECC) primarily used for?',
                'option_a': 'Drawing curves',
                'option_b': 'Providing same security as RSA with smaller key sizes',
                'option_c': 'Compressing data',
                'option_d': 'Network routing',
                'correct_answer': 'B',
                'difficulty': 'hard'
            },

            # Malware & Threats (10 questions)
            {
                'question_text': 'What is a computer virus?',
                'option_a': 'A hardware malfunction',
                'option_b': 'Malicious software that replicates itself',
                'option_c': 'A network protocol',
                'option_d': 'A type of encryption',
                'correct_answer': 'B',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is the difference between a virus and a worm?',
                'option_a': 'Viruses need a host file, worms spread independently',
                'option_b': 'Viruses are larger than worms',
                'option_c': 'Viruses are faster than worms',
                'option_d': 'There is no difference',
                'correct_answer': 'A',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is ransomware?',
                'option_a': 'Software that encrypts files and demands payment for decryption',
                'option_b': 'Software that steals passwords',
                'option_c': 'Software that displays advertisements',
                'option_d': 'Software that monitors keystrokes',
                'correct_answer': 'A',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is a Trojan horse in cybersecurity?',
                'option_a': 'A physical security device',
                'option_b': 'Malware disguised as legitimate software',
                'option_c': 'A type of firewall',
                'option_d': 'An encryption method',
                'correct_answer': 'B',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is a botnet?',
                'option_a': 'A legitimate network of robots',
                'option_b': 'A network of compromised computers controlled remotely',
                'option_c': 'A type of antivirus software',
                'option_d': 'A social networking site',
                'correct_answer': 'B',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is spyware?',
                'option_a': 'Software used by spies',
                'option_b': 'Software that secretly monitors and collects user information',
                'option_c': 'Software for video surveillance',
                'option_d': 'Software for network monitoring',
                'correct_answer': 'B',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is a rootkit?',
                'option_a': 'A gardening tool',
                'option_b': 'Malware that hides its presence on a system',
                'option_c': 'A network root directory',
                'option_d': 'A type of password',
                'correct_answer': 'B',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is adware?',
                'option_a': 'Software that displays unwanted advertisements',
                'option_b': 'Software for creating advertisements',
                'option_c': 'Software for blocking advertisements',
                'option_d': 'Software for managing advertisements',
                'correct_answer': 'A',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is a zero-day exploit?',
                'option_a': 'An exploit that costs zero dollars',
                'option_b': 'An exploit that takes zero days to develop',
                'option_c': 'An exploit for a vulnerability that has no available patch',
                'option_d': 'An exploit that works on day zero',
                'correct_answer': 'C',
                'difficulty': 'hard'
            },
            {
                'question_text': 'What is the primary purpose of antivirus software?',
                'option_a': 'To speed up computers',
                'option_b': 'To detect, prevent, and remove malware',
                'option_c': 'To encrypt files',
                'option_d': 'To backup data',
                'correct_answer': 'B',
                'difficulty': 'easy'
            },

            # Security Best Practices (10 questions)
            {
                'question_text': 'What makes a strong password?',
                'option_a': 'At least 8 characters with mix of letters, numbers, and symbols',
                'option_b': 'Using only lowercase letters',
                'option_c': 'Using only numbers',
                'option_d': 'Using your name',
                'correct_answer': 'A',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is two-factor authentication (2FA)?',
                'option_a': 'Using two passwords',
                'option_b': 'Using two different authentication methods',
                'option_c': 'Logging in twice',
                'option_d': 'Using two computers',
                'correct_answer': 'B',
                'difficulty': 'easy'
            },
            {
                'question_text': 'How often should software be updated?',
                'option_a': 'Never',
                'option_b': 'Once a year',
                'option_c': 'As soon as updates are available',
                'option_d': 'Only when problems occur',
                'correct_answer': 'C',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is social engineering?',
                'option_a': 'Building social networks',
                'option_b': 'Manipulating people to reveal confidential information',
                'option_c': 'Engineering social media platforms',
                'option_d': 'Creating social groups',
                'correct_answer': 'B',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is phishing?',
                'option_a': 'A fishing technique',
                'option_b': 'Attempting to obtain sensitive information through deceptive emails or websites',
                'option_c': 'A type of malware',
                'option_d': 'A network protocol',
                'correct_answer': 'B',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What should you do with suspicious emails?',
                'option_a': 'Open all attachments to check them',
                'option_b': 'Reply asking for more information',
                'option_c': 'Delete them without opening attachments or links',
                'option_d': 'Forward them to friends',
                'correct_answer': 'C',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is the principle of least privilege?',
                'option_a': 'Giving users maximum access',
                'option_b': 'Giving users only the minimum access needed for their job',
                'option_c': 'Giving no access to anyone',
                'option_d': 'Giving access based on seniority',
                'correct_answer': 'B',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is a security audit?',
                'option_a': 'A financial audit',
                'option_b': 'A systematic evaluation of security measures',
                'option_c': 'A type of malware scan',
                'option_d': 'A network speed test',
                'correct_answer': 'B',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is data backup important for?',
                'option_a': 'Saving storage space',
                'option_b': 'Speeding up computers',
                'option_c': 'Recovering data in case of loss or corruption',
                'option_d': 'Reducing network traffic',
                'correct_answer': 'C',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is the 3-2-1 backup rule?',
                'option_a': '3 computers, 2 networks, 1 backup',
                'option_b': '3 copies of data, 2 different media types, 1 offsite',
                'option_c': '3 passwords, 2 accounts, 1 administrator',
                'option_d': '3 firewalls, 2 antivirus programs, 1 IDS',
                'correct_answer': 'B',
                'difficulty': 'hard'
            }
        ]

        # Create questions in batches
        with transaction.atomic():
            questions_created = 0
            for question_data in questions_data:
                question, created = Question.objects.get_or_create(
                    subject=subject,
                    question_text=question_data['question_text'],
                    defaults={
                        'option_a': question_data['option_a'],
                        'option_b': question_data['option_b'],
                        'option_c': question_data['option_c'],
                        'option_d': question_data['option_d'],
                        'correct_answer': question_data['correct_answer'],
                        'difficulty': question_data['difficulty'],
                        'marks': 1,
                        'created_by': admin_user
                    }
                )
                if created:
                    questions_created += 1

            self.stdout.write(f'Created {questions_created} new questions')
            total_questions = Question.objects.filter(subject=subject).count()
            self.stdout.write(f'Total questions in Cybersecurity: {total_questions}')

        # Create the exam
        exam, created = Exam.objects.get_or_create(
            title='Cybersecurity Fundamentals Exam',
            subject=subject,
            defaults={
                'description': 'Comprehensive cybersecurity exam covering network security, encryption, malware, and security best practices. 15 questions will be randomly selected from a pool of 50.',
                'duration_minutes': 30,
                'questions_to_display': 15,
                'total_marks': 15,
                'is_active': True,
                'randomize_questions': True,
                'show_results_immediately': True,
                'created_by': admin_user
            }
        )

        if created:
            # Add all questions to the exam
            all_questions = Question.objects.filter(subject=subject)
            for i, question in enumerate(all_questions):
                exam.examquestion_set.create(question=question, order=i)
            
            self.stdout.write(self.style.SUCCESS(f'Created exam: {exam.title}'))
            self.stdout.write(f'Exam configured to show {exam.questions_to_display} random questions out of {exam.questions.count()} total questions')
        else:
            self.stdout.write(f'Exam "{exam.title}" already exists')

        self.stdout.write(self.style.SUCCESS('Cybersecurity course setup completed!'))
        self.stdout.write('Students will see 15 randomly selected questions from the pool of 50 when taking the exam.')
