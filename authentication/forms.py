from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import CustomUser, CourseEnrollment

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number (optional)'
        })
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    course = forms.ModelChoiceField(
        queryset=None,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text="Select the N-TECH course you want to enroll in"
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'course', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import here to avoid circular import
        from exams.models import Course
        self.fields['course'].queryset = Course.objects.filter(is_active=True)
        
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

    def save(self, commit=True):
        from .models import CourseEnrollment
        
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.user_type = 'student'
        user.is_approved = True  # Students are auto-approved
        if commit:
            user.save()
            # Enroll student in selected course
            CourseEnrollment.objects.create(
                student=user,
                course=self.cleaned_data['course'],
                is_active=True
            )
        return user


class InstructorRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number (optional)'
        })
    )
    institution = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'School/University/Institution name'
        }),
        help_text="Name of your educational institution"
    )
    department = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your department (e.g., Computer Science, Mathematics)'
        })
    )
    specialization = forms.MultipleChoiceField(
        choices=[
            ('fullstack', 'Full Stack Web Development'),
            ('frontend_react', 'Frontend Development with React.js'),
            ('backend_django', 'Backend Development with Python Django'),
            ('backend_fastapi', 'Backend Development with FastAPI'),
            ('data_analysis', 'Data Analysis'),
            ('data_science', 'Data Science'),
            ('cybersecurity', 'Cybersecurity'),
            ('ui_ux', 'UI/UX Design'),
            ('mobile_dev', 'Mobile Development'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=True,
        help_text="Select the N-TECH courses you are qualified to teach"
    )
    bio = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Brief description about yourself and your teaching background',
            'rows': 4
        }),
        help_text="Tell us about your teaching experience and qualifications"
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'institution', 'department', 'specialization', 'bio', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.institution = self.cleaned_data['institution']
        user.department = self.cleaned_data['department']
        # Store specialization in bio for now (can be moved to separate field later)
        specializations = ', '.join(dict(self.fields['specialization'].choices)[spec] for spec in self.cleaned_data['specialization'])
        user.bio = f"Specializations: {specializations}\n\n{self.cleaned_data['bio']}"
        user.user_type = 'instructor'
        user.is_approved = False  # Instructors need approval from super admin
        if commit:
            user.save()
        return user

class SimpleLoginForm(forms.Form):
    """Simple login form that doesn't inherit from AuthenticationForm"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            # Try to authenticate
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password.")
            elif not user.is_active:
                raise forms.ValidationError("This account is disabled.")
            elif user.user_type == 'instructor' and not user.is_approved:
                raise forms.ValidationError("Your instructor account is pending approval. Please contact the administrator.")
            
            # Store the user for the view
            self.user = user
        
        return cleaned_data

class CustomPasswordResetForm(PasswordResetForm):
    """Custom password reset form with N-TECH styling"""
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autofocus': True
        }),
        help_text="Enter the email address associated with your N-TECH account."
    )

    def clean_email(self):
        """Validate that the email exists in our system"""
        email = self.cleaned_data['email']
        
        # Check if user exists and is active
        try:
            user = CustomUser.objects.get(email=email, is_active=True)
        except CustomUser.DoesNotExist:
            raise ValidationError(
                "No account found with this email address. Please check your email or contact support."
            )
        
        # Check if instructor is approved
        if user.user_type == 'instructor' and not user.is_approved:
            raise ValidationError(
                "Your instructor account is pending approval. Please contact the administrator for assistance."
            )
        
        return email

    def get_users(self, email):
        """Return matching user(s) who should receive a reset.
        
        This allows us to more easily customize this later if needed.
        """
        active_users = CustomUser.objects.filter(
            email__iexact=email,
            is_active=True,
        )
        return (
            u for u in active_users
            if u.has_usable_password() and
            self._validate_user_permissions(u)
        )

    def _validate_user_permissions(self, user):
        """Validate user permissions for password reset"""
        # Students are always allowed to reset
        if user.user_type == 'student':
            return True
        
        # Instructors must be approved
        if user.user_type == 'instructor':
            return user.is_approved
        
        # Admins and superusers are allowed
        if user.user_type == 'admin' or user.is_superuser:
            return True
        
        return False

class CustomSetPasswordForm(SetPasswordForm):
    """Custom set password form with N-TECH styling and validation"""
    
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password',
            'autocomplete': 'new-password'
        }),
        strip=False,
        help_text="Your password must be at least 8 characters long and contain letters and numbers."
    )
    
    new_password2 = forms.CharField(
        label="Confirm new password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password',
            'autocomplete': 'new-password'
        }),
    )

    def clean_new_password1(self):
        """Add custom validation for password strength"""
        password = self.cleaned_data.get('new_password1')
        
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        if password.isdigit():
            raise ValidationError("Password cannot be entirely numeric.")
        
        if not any(char.isalpha() for char in password):
            raise ValidationError("Password must contain at least one letter.")
        
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one number.")
        
        return password


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information"""
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'institution', 'department']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your institution/school'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your department'
            }),
        }


class CourseEnrollmentForm(forms.Form):
    """Form for managing course enrollments"""
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        # Import here to avoid circular import
        from exams.models import Course
        
        # Get all available courses
        all_courses = Course.objects.filter(is_active=True)
        
        # Get user's current enrollments
        current_enrollments = CourseEnrollment.objects.filter(
            student=user, 
            is_active=True
        ).values_list('course_id', flat=True)
        
        # Create checkboxes for each course
        for course in all_courses:
            field_name = f'course_{course.id}'
            self.fields[field_name] = forms.BooleanField(
                label=course.name,
                required=False,
                initial=course.id in current_enrollments,
                widget=forms.CheckboxInput(attrs={
                    'class': 'form-check-input'
                })
            )
            # Store course info for later use
            self.fields[field_name].course = course
    
    def save(self):
        """Update user's course enrollments"""
        from exams.models import Course
        
        # Get current enrollments
        current_enrollments = list(CourseEnrollment.objects.filter(
            student=self.user, 
            is_active=True
        ))
        
        # Collect selected courses
        selected_course_ids = []
        for field_name, field in self.fields.items():
            if field_name.startswith('course_') and self.cleaned_data.get(field_name):
                course_id = int(field_name.split('_')[1])
                selected_course_ids.append(course_id)
        
        # Get currently enrolled course IDs
        currently_enrolled_ids = [enrollment.course.id for enrollment in current_enrollments]
        
        # Deactivate courses that are no longer selected
        for enrollment in current_enrollments:
            if enrollment.course.id not in selected_course_ids:
                enrollment.is_active = False
                enrollment.save()
        
        # Add new enrollments for newly selected courses
        for course_id in selected_course_ids:
            if course_id not in currently_enrolled_ids:
                # Check if there's an inactive enrollment we can reactivate
                existing_enrollment = CourseEnrollment.objects.filter(
                    student=self.user,
                    course_id=course_id
                ).first()
                
                if existing_enrollment:
                    existing_enrollment.is_active = True
                    existing_enrollment.save()
                else:
                    # Create new enrollment
                    course = Course.objects.get(id=course_id)
                    CourseEnrollment.objects.create(
                        student=self.user,
                        course=course,
                        is_active=True
                    )


class QuickCourseChangeForm(forms.Form):
    """Simplified form for quickly changing primary course"""
    
    course = forms.ModelChoiceField(
        queryset=None,
        required=True,
        empty_label="Select a course",
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text="Select your primary course of study"
    )
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        # Import here to avoid circular import
        from exams.models import Course
        
        self.fields['course'].queryset = Course.objects.filter(is_active=True)
        
        # Set current course as initial value
        current_enrollment = CourseEnrollment.objects.filter(
            student=user, 
            is_active=True
        ).first()
        
        if current_enrollment:
            self.fields['course'].initial = current_enrollment.course
    
    def save(self):
        """Change user's primary course enrollment"""
        selected_course = self.cleaned_data['course']
        
        # Deactivate all current enrollments
        CourseEnrollment.objects.filter(
            student=self.user, 
            is_active=True
        ).update(is_active=False)
        
        # Check if user was previously enrolled in this course
        existing_enrollment = CourseEnrollment.objects.filter(
            student=self.user,
            course=selected_course
        ).first()
        
        if existing_enrollment:
            # Reactivate existing enrollment
            existing_enrollment.is_active = True
            existing_enrollment.save()
        else:
            # Create new enrollment
            CourseEnrollment.objects.create(
                student=self.user,
                course=selected_course,
                is_active=True
            )
