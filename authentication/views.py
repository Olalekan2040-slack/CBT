from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .models import CustomUser
from .forms import StudentRegistrationForm, InstructorRegistrationForm, SimpleLoginForm, CustomPasswordResetForm, CustomSetPasswordForm
import uuid
import logging

logger = logging.getLogger(__name__)

def send_verification_email(user, request):
    """Send email verification email to user"""
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = str(user.email_verification_token)
    
    verification_url = request.build_absolute_uri(
        reverse('authentication:verify_email', kwargs={'uid': uid, 'token': token})
    )
    
    subject = 'Verify Your N-TECH CBT Account'
    message = render_to_string('authentication/verification_email.html', {
        'user': user,
        'verification_url': verification_url,
        'site_name': current_site.name,
    })
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=message,
            fail_silently=False
        )
        logger.info(f"Verification email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send verification email to {user.email}: {str(e)}")
        return False

def register_choice(request):
    """Let users choose between student and instructor registration"""
    return render(request, 'authentication/register_choice.html')

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create user but don't activate yet
                user = form.save(commit=False)
                user.is_active = False  # User must verify email first
                user.is_email_verified = False
                user.email_verification_token = uuid.uuid4()
                user.save()
                
                # Send verification email
                if send_verification_email(user, request):
                    messages.success(
                        request, 
                        f'Registration successful! Please check your email ({user.email}) '
                        'and click the verification link to activate your account.'
                    )
                    return redirect('authentication:login')
                else:
                    messages.error(
                        request, 
                        'Registration successful but we could not send the verification email. '
                        'Please contact support.'
                    )
                    return redirect('authentication:login')
                    
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
                print(f"Registration error: {e}")
        else:
            # Add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'authentication/student_register.html', {'form': form})

def instructor_register(request):
    if request.method == 'POST':
        form = InstructorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.info(request, 
                f'Welcome to N-TECH! Your instructor account has been created successfully. '
                f'Your application is pending approval by our administrators. '
                f'You will receive an email notification once approved to start creating courses and assessments.')
            
            # Send approval pending email to instructor
            try:
                send_mail(
                    'N-TECH CBT - Instructor Account Pending Approval',
                    f'Hello {user.first_name},\n\nThank you for applying to become an N-TECH instructor!\n\nYour account details:\n- Name: {user.get_full_name()}\n- Institution: {user.institution}\n- Department: {user.department}\n- Specializations: {", ".join(user.specializations) if user.specializations else "Not specified"}\n\nYour instructor application is currently under review by our administrators. You will receive an email notification once your account is approved and you can start creating technology training content.\n\nBest regards,\nN-TECH Training Team',
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
            
            # Check if email is verified for non-superusers
            if not user.is_superuser and not user.is_email_verified:
                messages.error(
                    request, 
                    'Please verify your email address before logging in. '
                    f'<a href="{reverse("authentication:resend_verification")}">Resend verification email</a>'
                )
                return render(request, 'authentication/login.html', {'form': form})
            
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
@require_POST
@csrf_protect
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')

class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view with N-TECH branding"""
    form_class = CustomPasswordResetForm
    template_name = 'authentication/password_reset.html'
    email_template_name = 'authentication/password_reset_email.html'
    subject_template_name = 'authentication/password_reset_subject.txt'
    success_url = reverse_lazy('authentication:password_reset_done')
    
    def form_valid(self, form):
        """Send password reset email with custom messaging"""
        messages.success(
            self.request,
            'Password reset instructions have been sent to your email address. '
            'Please check your inbox and follow the instructions to reset your password.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle invalid form submission"""
        messages.error(
            self.request,
            'Please correct the errors below and try again.'
        )
        return super().form_invalid(form)

def password_reset_done(request):
    """Password reset done view"""
    return render(request, 'authentication/password_reset_done.html')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Custom password reset confirm view"""
    form_class = CustomSetPasswordForm
    template_name = 'authentication/password_reset_confirm.html'
    success_url = reverse_lazy('authentication:password_reset_complete')
    
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context['validlink'] = False
            messages.error(self.request, 'This password reset link is invalid or has expired.')
        return context
    
    def form_valid(self, form):
        """Handle successful password reset"""
        messages.success(
            self.request,
            'Your password has been successfully reset! You can now login with your new password.'
        )
        return super().form_valid(form)

def password_reset_complete(request):
    """Password reset complete view"""
    return render(request, 'authentication/password_reset_complete.html')

def verify_email(request, uid, token):
    """Verify user's email address"""
    try:
        # Decode the user ID
        user_id = force_str(urlsafe_base64_decode(uid))
        user = get_object_or_404(CustomUser, pk=user_id)
        
        # Check if token matches
        if str(user.email_verification_token) == token:
            if not user.is_email_verified:
                user.is_email_verified = True
                user.is_active = True  # Activate the account
                user.save()
                
                messages.success(
                    request, 
                    'Email verified successfully! You can now log in to your account.'
                )
                return redirect('authentication:login')
            else:
                messages.info(request, 'Your email is already verified.')
                return redirect('authentication:login')
        else:
            messages.error(request, 'Invalid verification link.')
            return redirect('authentication:login')
            
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        messages.error(request, 'Invalid verification link.')
        return redirect('authentication:login')

def resend_verification_email(request):
    """Resend verification email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email, is_email_verified=False)
            # Generate new token
            user.email_verification_token = uuid.uuid4()
            user.save()
            
            if send_verification_email(user, request):
                messages.success(
                    request, 
                    f'Verification email sent to {email}. Please check your inbox.'
                )
            else:
                messages.error(
                    request, 
                    'Failed to send verification email. Please try again later.'
                )
        except CustomUser.DoesNotExist:
            messages.error(
                request, 
                'No unverified account found with this email address.'
            )
        
        return redirect('authentication:login')
    
    return render(request, 'authentication/resend_verification.html')
