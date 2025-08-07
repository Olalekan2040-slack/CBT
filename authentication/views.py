from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from .forms import StudentRegistrationForm, InstructorRegistrationForm, SimpleLoginForm

def register_choice(request):
    """Let users choose between student and instructor registration"""
    return render(request, 'authentication/register_choice.html')

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Student account created successfully! You can now login.')
            
            # Send welcome email
            try:
                send_mail(
                    'Welcome to CBT System - Student Account',
                    f'Hello {user.first_name},\n\nWelcome to our Computer-Based Testing System! Your student account has been created successfully.\n\nYou can now log in and start taking exams.\n\nBest regards,\nCBT System Team',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            return redirect('authentication:login')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'authentication/student_register.html', {'form': form})

def instructor_register(request):
    if request.method == 'POST':
        form = InstructorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.info(request, 
                'Instructor account created successfully! Your account is pending approval. '
                'You will receive an email once approved by the administrator.')
            
            # Send approval pending email to instructor
            try:
                send_mail(
                    'CBT System - Instructor Account Pending Approval',
                    f'Hello {user.first_name},\n\nThank you for registering as an instructor on our CBT System.\n\nYour account details:\n- Name: {user.get_full_name()}\n- Institution: {user.institution}\n- Department: {user.department}\n\nYour account is currently pending approval by the system administrator. You will receive an email notification once your account is approved.\n\nBest regards,\nCBT System Team',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            return redirect('authentication:login')
    else:
        form = InstructorRegistrationForm()
    
    return render(request, 'authentication/instructor_register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = SimpleLoginForm(request.POST)
        
        if form.is_valid():
            user = form.user  # Get the authenticated user from the form
            login(request, user)
            
            # Redirect based on user type
            if user.is_superuser:
                messages.success(request, f'Welcome back, Super Admin!')
                return redirect('/admin/')
            elif user.is_instructor:
                messages.success(request, f'Welcome back, Instructor {user.get_full_name()}!')
                return redirect('core:dashboard')
            else:
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('core:dashboard')
        else:
            # Form errors will be displayed in the template
            pass
    else:
        form = SimpleLoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})

# Legacy view for backward compatibility
def register_view(request):
    return redirect('authentication:register_choice')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')
