from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Course(models.Model):
    """N-TECH training courses"""
    COURSE_CHOICES = [
        ('fullstack', 'Full Stack Web Development'),
        ('frontend_react', 'Frontend Development with React.js'),
        ('backend_django', 'Backend Development with Python Django'),
        ('backend_fastapi', 'Backend Development with FastAPI'),
        ('data_analysis', 'Data Analysis'),
        ('data_science', 'Data Science'),
        ('cybersecurity', 'Cybersecurity'),
        ('ui_ux', 'UI/UX Design'),
        ('mobile_dev', 'Mobile Development'),
    ]
    
    code = models.CharField(max_length=20, choices=COURSE_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration_weeks = models.PositiveIntegerField(default=12, help_text="Course duration in weeks")
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'user_type': 'instructor'},
        related_name='assigned_courses'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        course_name = self.course.name if self.course else "No Course"
        return f"{course_name} - {self.name}"
    
    class Meta:
        unique_together = ('course', 'name')

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    marks = models.PositiveIntegerField(default=1)
    explanation = models.TextField(blank=True, help_text="Explanation for the correct answer")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        course_name = self.course.name if self.course else "No Course"
        return f"{course_name} - {self.subject.name} - {self.question_text[:50]}..."
    
    def save(self, *args, **kwargs):
        # Auto-assign course from subject if not provided
        if not self.course and self.subject:
            self.course = self.subject.course
        # Ensure subject belongs to the same course
        if self.subject and self.course and self.subject.course != self.course:
            raise ValueError("Subject must belong to the same course")
        super().save(*args, **kwargs)

class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams', null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, through='ExamQuestion')
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    total_marks = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    randomize_questions = models.BooleanField(default=True)
    questions_to_display = models.PositiveIntegerField(
        default=10, 
        help_text="Number of questions to randomly display to students. Leave blank to use all questions."
    )
    show_results_immediately = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        course_name = self.course.name if self.course else "No Course"
        return f"{course_name} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Auto-assign course from subject if not provided
        if not self.course and self.subject:
            self.course = self.subject.course
        # Ensure subject belongs to the same course
        if self.subject and self.course and self.subject.course != self.course:
            raise ValueError("Subject must belong to the same course")
        super().save(*args, **kwargs)

class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ('exam', 'question')
        ordering = ['order']

class ExamAttempt(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('timeout', 'Timeout'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    selected_questions = models.ManyToManyField(Question, blank=True, help_text="Questions randomly selected for this attempt")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    time_taken_minutes = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ('student', 'exam')
    
    def __str__(self):
        return f"{self.student.email} - {self.exam.title} - {self.status}"

class StudentAnswer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('attempt', 'question')
    
    def save(self, *args, **kwargs):
        self.is_correct = (self.selected_answer == self.question.correct_answer)
        super().save(*args, **kwargs)
