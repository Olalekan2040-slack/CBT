# CBT System - Computer Based Testing Platform

A comprehensive Computer Based Testing (CBT) system built with Django, featuring multi-level user management, random question selection, and real-time exam monitoring.

## Features

### 🔐 Multi-Level Authentication
- **Students**: Auto-approved registration, can take exams
- **Instructors**: Require admin approval, can create questions and exams
- **Super Admin**: Approves instructors, manages entire system

### 📝 Exam Management
- Create subjects and questions with multiple difficulty levels
- Set up exams with configurable parameters:
  - Duration control
  - Random question selection from question pools
  - Customizable number of questions to display
  - Real-time timer with automatic submission

### 🎯 Advanced Question System
- Support for multiple choice questions (A, B, C, D)
- Question difficulty levels (Easy, Medium, Hard)
- Explanation support for correct answers
- Questions organized by subjects

### 📊 Performance Tracking
- Detailed exam results with percentage scores
- Student performance analytics
- Instructor dashboard with student statistics
- Admin oversight of all system activities

### 🎨 User Interface
- Dark theme with Bootstrap 5.3
- Responsive design for all devices
- Intuitive navigation and user experience
- Real-time exam interface with progress tracking

## Technology Stack

- **Backend**: Django 5.2.1
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: Bootstrap 5.3, HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in authentication with custom user model
- **Email**: Django email system for notifications

## Project Structure

```
CBT/
├── authentication/          # User management and authentication
├── core/                   # Main application logic and dashboards
├── exams/                  # Exam, question, and attempt management
├── static/                 # Static files (CSS, JS, images)
├── templates/              # HTML templates
├── cbt_system/            # Project settings and configuration
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Olalekan2040-slack/CBT.git
   cd CBT
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load sample data (optional)**
   ```bash
   python manage.py create_cybersecurity_course
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Usage

### For Students
1. Register at `/auth/register/student/`
2. Login and access available exams from dashboard
3. Take exams with real-time timer
4. View results immediately after submission

### For Instructors
1. Register at `/auth/register/instructor/`
2. Wait for admin approval
3. Once approved, create questions and exams
4. Monitor student performance through instructor dashboard

### For Administrators
1. Access Django admin at `/admin/`
2. Approve pending instructor registrations
3. Monitor all system activities
4. Manage subjects, questions, and exams

## Key Features Implemented

### Random Question Selection
- Exams can be configured to show a subset of questions from a larger pool
- Example: 15 questions randomly selected from 50 available questions
- Each student gets a different set of questions for fair assessment

### Real-time Exam System
- Automatic timer with countdown display
- Auto-submission when time expires
- Progress tracking during exam
- Prevention of multiple attempts

### Comprehensive Reporting
- Individual student performance reports
- Instructor analytics showing student progress
- System-wide statistics for administrators
- Email notifications for exam results

## Sample Data

The system includes a pre-built Cybersecurity course with:
- 50 comprehensive questions covering:
  - Network Security (15 questions)
  - Encryption & Cryptography (15 questions)
  - Malware & Threats (10 questions)
  - Security Best Practices (10 questions)
- Configured to display 15 random questions per exam
- 30-minute duration with immediate results

## Configuration

### Email Settings
Configure email settings in `settings.py` for result notifications:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@domain.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

### Database Configuration
For production, update database settings in `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cbt_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please create an issue on GitHub or contact the development team.

## Roadmap

- [ ] Add support for different question types (True/False, Fill-in-the-blank)
- [ ] Implement exam scheduling and time windows
- [ ] Add plagiarism detection
- [ ] Mobile app development
- [ ] Advanced analytics and reporting
- [ ] Integration with Learning Management Systems (LMS)

---

**CBT System** - Making computer-based testing simple, secure, and scalable. System - Computer-Based Testing Platform

A comprehensive web-based testing platform built with Django and featuring a modern dark-themed interface with animations.

## Features

### 🎯 Core Features
- **User Authentication**: Custom user model with separate student and admin roles
- **Exam Management**: Admins can create and manage up to 1000+ multiple choice questions
- **Random Question Selection**: Questions are randomly shuffled for each student
- **Timed Examinations**: Configurable timer with automatic submission
- **Email Results**: Automatic email delivery of exam results to students
- **Auto-save**: Answers are automatically saved to prevent data loss
- **Responsive Design**: Works seamlessly on all devices

### 🎨 Frontend Features
- **Dark Theme**: Modern dark UI with animated components
- **Real-time Timer**: Visual countdown with warnings
- **Progress Tracking**: Live progress bar showing completion status
- **Smooth Animations**: CSS animations and transitions throughout
- **Mobile Responsive**: Optimized for all screen sizes

### 🔐 Security Features
- **Secure Authentication**: Email-based login system
- **Session Management**: Automatic session timeout
- **CSRF Protection**: Built-in Django security features
- **Data Validation**: Comprehensive form validation

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Start

1. **Clone/Download the project**
   ```bash
   # Navigate to your project directory
   cd "c:\Users\DELL\Documents\Personal\CBT"
   ```

2. **Install Dependencies**
   ```bash
   pip install django
   ```

3. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Sample Data**
   ```bash
   python manage.py populate_data
   ```

5. **Start the Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**
   - Open your web browser and go to: `http://127.0.0.1:8000/`

## Demo Accounts

The system comes with pre-created demo accounts:

### Admin Account
- **Email**: `admin@cbt.com`
- **Password**: `admin123`
- **Access**: Full admin panel access, can create/manage questions and exams

### Student Account
- **Email**: `student@cbt.com`
- **Password**: `student123`
- **Access**: Can take exams and view results

## Usage Guide

### For Administrators

1. **Login** with admin credentials
2. **Access Admin Panel** at `http://127.0.0.1:8000/admin/`
3. **Create Subjects**: Add different subject categories
4. **Add Questions**: Create multiple choice questions (up to 1000+)
5. **Create Exams**: Set up exams with selected questions and time limits
6. **Monitor Results**: View student attempts and performance

### For Students

1. **Register** a new account or **Login** with existing credentials
2. **View Available Exams** on the dashboard
3. **Start an Exam**: Click "Start Exam" button
4. **Take the Test**: 
   - Answer questions within the time limit
   - Timer shows remaining time with visual warnings
   - Progress bar shows completion status
   - Answers are auto-saved
5. **Submit**: Click "Submit Exam" when finished
6. **View Results**: Instant results with detailed breakdown
7. **Email**: Results are automatically sent to your email

## Project Structure

```
CBT/
├── cbt_system/          # Django project settings
├── authentication/     # User authentication app
├── core/               # Main application logic
├── exams/              # Exam and question management
├── templates/          # HTML templates
├── static/             # CSS, JavaScript, images
├── media/              # User uploaded files
└── manage.py           # Django management script
```

## Key Models

### CustomUser
- Extended Django user model
- Email-based authentication
- Student/Admin role separation

### Subject
- Category for questions (Math, Science, etc.)

### Question
- Multiple choice questions with 4 options
- Difficulty levels (Easy, Medium, Hard)
- Configurable marks per question

### Exam
- Collection of questions
- Time limits and scheduling
- Random question ordering

### ExamAttempt
- Student exam sessions
- Time tracking and scoring
- Status management

## Email Configuration

To enable email functionality:

1. **Update settings.py**:
   ```python
   EMAIL_HOST_USER = 'your-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-app-password'
   ```

2. **For Gmail**:
   - Enable 2-factor authentication
   - Generate an app-specific password
   - Use the app password in settings

## Technical Stack

- **Backend**: Django 5.2.1
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Bootstrap 5.3 + Custom CSS
- **JavaScript**: jQuery + Vanilla JS
- **Icons**: Font Awesome 6.4
- **Animations**: Animate.css

## Features in Detail

### Timer System
- Real-time countdown display
- Visual warnings (5 minutes, 1 minute)
- Automatic submission when time expires
- Mobile-responsive timer positioning

### Question Randomization
- Questions shuffled for each attempt
- Prevents cheating through question order
- Configurable per exam

### Auto-save Functionality
- Answers saved every 30 seconds
- Immediate save on answer selection
- Prevents data loss on connection issues

### Email System
- Automated result delivery
- Detailed performance breakdown
- Professional email templates

## Customization

### Themes
- Easily customizable color scheme in `static/css/style.css`
- Dark theme with support for light theme toggle

### Question Types
- Currently supports multiple choice (A, B, C, D)
- Extendable for true/false, multiple select, etc.

### Scoring
- Configurable marks per question
- Automatic score calculation
- Percentage-based results

## Deployment

### Production Deployment
1. **Update settings** for production
2. **Configure database** (PostgreSQL recommended)
3. **Set up email** service (SendGrid, Mailgun, etc.)
4. **Configure static files** serving
5. **Use WSGI server** (Gunicorn, uWSGI)
6. **Set up reverse proxy** (Nginx, Apache)

### Environment Variables
```bash
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For support or questions:
- Create an issue in the repository
- Check the documentation
- Review the demo accounts and sample data

## Version History

- **v1.0.0**: Initial release with core CBT functionality
- Complete user authentication system
- Exam creation and management
- Real-time timer and auto-submission
- Email result delivery
- Responsive dark theme UI

---

**Note**: This is a development version. For production use, please ensure proper security configurations, use a production database, and set up proper email services.
