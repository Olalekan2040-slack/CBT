from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from exams.models import Exam, ExamAttempt, Question
from authentication.models import CustomUser

def home(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    context = {}
    
    if request.user.is_student:
        # Student dashboard
        available_exams = Exam.objects.filter(is_active=True).exclude(
            examattempt__student=request.user
        )
        completed_attempts = ExamAttempt.objects.filter(
            student=request.user, 
            status='completed'
        ).order_by('-start_time')
        
        context.update({
            'available_exams': available_exams,
            'completed_attempts': completed_attempts,
            'total_completed': completed_attempts.count(),
        })
        
        return render(request, 'core/student_dashboard.html', context)
    
    elif request.user.is_instructor:
        # Instructor dashboard - shows their created content and student performance
        instructor_questions = Question.objects.filter(created_by=request.user)
        instructor_exams = Exam.objects.filter(created_by=request.user)
        
        # Students who took instructor's exams
        student_attempts = ExamAttempt.objects.filter(
            exam__created_by=request.user
        ).select_related('student', 'exam').order_by('-start_time')
        
        # Statistics for instructor
        total_questions_created = instructor_questions.count()
        total_exams_created = instructor_exams.count()
        total_student_attempts = student_attempts.count()
        unique_students = student_attempts.values('student').distinct().count()
        
        context.update({
            'instructor_questions': instructor_questions[:10],  # Latest 10
            'instructor_exams': instructor_exams,
            'student_attempts': student_attempts[:20],  # Latest 20
            'total_questions_created': total_questions_created,
            'total_exams_created': total_exams_created,
            'total_student_attempts': total_student_attempts,
            'unique_students': unique_students,
        })
        
        return render(request, 'core/instructor_dashboard.html', context)
    
    elif request.user.is_admin or request.user.is_superuser:
        # Super Admin dashboard - shows everything
        total_exams = Exam.objects.count()
        active_exams = Exam.objects.filter(is_active=True).count()
        total_questions = Question.objects.count()
        total_students = CustomUser.objects.filter(user_type='student').count()
        total_instructors = CustomUser.objects.filter(user_type='instructor').count()
        pending_instructors = CustomUser.objects.filter(user_type='instructor', is_approved=False).count()
        total_attempts = ExamAttempt.objects.count()
        
        recent_attempts = ExamAttempt.objects.select_related(
            'student', 'exam'
        ).order_by('-start_time')[:15]
        
        recent_instructor_registrations = CustomUser.objects.filter(
            user_type='instructor', is_approved=False
        ).order_by('-date_joined')[:5]
        
        context.update({
            'total_exams': total_exams,
            'active_exams': active_exams,
            'total_questions': total_questions,
            'total_students': total_students,
            'total_instructors': total_instructors,
            'pending_instructors': pending_instructors,
            'total_attempts': total_attempts,
            'recent_attempts': recent_attempts,
            'recent_instructor_registrations': recent_instructor_registrations,
        })
        
        return render(request, 'core/admin_dashboard.html', context)
    
    return render(request, 'core/dashboard.html', context)
