from django.urls import path
from . import views
from .test_views import test_login

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_choice, name='register'),
    path('register/student/', views.student_register, name='student_register'),
    path('register/instructor/', views.instructor_register, name='instructor_register'),
    
    # Email Verification URLs
    path('verify-email/<uid>/<token>/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification_email, name='resend_verification'),
    
    # Password Reset URLs
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.password_reset_done, name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.password_reset_complete, name='password_reset_complete'),
    
    path('test-login/', test_login, name='test_login'),  # Debug URL
]
