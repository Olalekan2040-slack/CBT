from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    is_approved = models.BooleanField(default=False, help_text="Approved by super admin")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    institution = models.CharField(max_length=200, blank=True, help_text="School/University/Institution")
    department = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True, help_text="Brief description about the instructor")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def get_enrolled_courses(self):
        """Get courses the user is enrolled in"""
        from exams.models import Course
        if hasattr(self, 'course_enrollments'):
            return Course.objects.filter(enrollments__student=self, enrollments__is_active=True)
        return Course.objects.none()
    
    def get_assigned_courses(self):
        """Get courses assigned to instructor"""
        if self.is_instructor:
            from exams.models import Course
            return Course.objects.filter(instructor=self)
        return Course.objects.none()
    
    @property
    def is_student(self):
        return self.user_type == 'student'
    
    @property
    def is_instructor(self):
        return self.user_type == 'instructor' and self.is_approved
    
    @property
    def is_admin(self):
        return self.user_type == 'admin' or self.is_superuser

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class CourseEnrollment(models.Model):
    """Track student enrollments in N-TECH courses"""
    student = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='course_enrollments',
        limit_choices_to={'user_type': 'student'}
    )
    course = models.ForeignKey('exams.Course', on_delete=models.CASCADE, related_name='enrollments')
    enrolled_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ('student', 'course')
        verbose_name = "Course Enrollment"
        verbose_name_plural = "Course Enrollments"
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.course.name}"
