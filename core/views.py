from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from exams.models import Exam, ExamAttempt, Question, Course
from authentication.models import CustomUser

def home(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    # Show N-TECH course information
    courses = Course.objects.filter(is_active=True).order_by('name')
    context = {
        'courses': courses,
        'total_courses': courses.count(),
    }
    return render(request, 'core/home.html', context)

@login_required
def dashboard(request):
    context = {}
    
    if request.user.is_student:
        # Student dashboard - show only exams for their enrolled courses
        enrolled_courses = request.user.get_enrolled_courses()
        available_exams = Exam.objects.filter(
            is_active=True,
            course__in=enrolled_courses
        ).exclude(
            examattempt__student=request.user
        )
        completed_attempts = ExamAttempt.objects.filter(
            student=request.user, 
            status='completed'
        ).order_by('-start_time')
        
        # Calculate latest score percentage safely
        latest_score_percentage = 0
        if completed_attempts.exists():
            latest_attempt = completed_attempts.first()
            if latest_attempt.exam.total_marks > 0:
                latest_score_percentage = round((latest_attempt.score / latest_attempt.exam.total_marks) * 100, 1)
        
        context.update({
            'enrolled_courses': enrolled_courses,
            'available_exams': available_exams,
            'completed_attempts': completed_attempts,
            'total_completed': completed_attempts.count(),
            'latest_score_percentage': latest_score_percentage,
        })
        
        return render(request, 'core/student_dashboard.html', context)
    
    elif request.user.is_instructor:
        # Instructor dashboard - shows their assigned courses and student performance
        assigned_courses = request.user.get_assigned_courses()
        instructor_questions = Question.objects.filter(
            created_by=request.user,
            course__in=assigned_courses
        )
        instructor_exams = Exam.objects.filter(
            created_by=request.user,
            course__in=assigned_courses
        )
        
        # Students who took instructor's exams
        student_attempts = ExamAttempt.objects.filter(
            exam__created_by=request.user,
            exam__course__in=assigned_courses
        ).select_related('student', 'exam').order_by('-start_time')
        
        # Statistics for instructor
        total_questions_created = instructor_questions.count()
        total_exams_created = instructor_exams.count()
        total_student_attempts = student_attempts.count()
        unique_students = student_attempts.values('student').distinct().count()
        
        context.update({
            'assigned_courses': assigned_courses,
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
        total_courses = Course.objects.count()
        active_courses = Course.objects.filter(is_active=True).count()
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
        
        # Course enrollment statistics
        from authentication.models import CourseEnrollment
        course_stats = []
        for course in Course.objects.filter(is_active=True):
            enrollment_count = CourseEnrollment.objects.filter(course=course, is_active=True).count()
            course_stats.append({
                'course': course,
                'enrollments': enrollment_count
            })
        
        context.update({
            'total_courses': total_courses,
            'active_courses': active_courses,
            'total_exams': total_exams,
            'active_exams': active_exams,
            'total_questions': total_questions,
            'total_students': total_students,
            'total_instructors': total_instructors,
            'pending_instructors': pending_instructors,
            'total_attempts': total_attempts,
            'recent_attempts': recent_attempts,
            'recent_instructor_registrations': recent_instructor_registrations,
            'course_stats': course_stats,
        })
        
        return render(request, 'core/admin_dashboard.html', context)
    
    return render(request, 'core/dashboard.html', context)
