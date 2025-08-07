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
    path('test-login/', test_login, name='test_login'),  # Debug URL
]
