from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser

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
