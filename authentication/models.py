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
