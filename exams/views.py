from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import random
from datetime import timedelta
from .models import Exam, ExamAttempt, Question, StudentAnswer

@login_required
def exam_list(request):
    if not request.user.is_student:
        messages.error(request, 'Only students can access this page.')
        return redirect('core:dashboard')
    
    # Get enrolled courses for the student
    from authentication.models import CourseEnrollment
    enrolled_courses = CourseEnrollment.objects.filter(
        student=request.user, 
        is_active=True
    ).values_list('course', flat=True)
    
    # Only show exams for courses the student is enrolled in
    available_exams = Exam.objects.filter(
        is_active=True,
        course__in=enrolled_courses
    ).exclude(
        examattempt__student=request.user
    )
    
    return render(request, 'exams/exam_list.html', {
        'available_exams': available_exams
    })

@login_required
def start_exam(request, exam_id):
    if not request.user.is_student:
        messages.error(request, 'Only students can take exams.')
        return redirect('core:dashboard')
    
    exam = get_object_or_404(Exam, id=exam_id, is_active=True)
    
    # Check if student is enrolled in the exam's course
    from authentication.models import CourseEnrollment
    is_enrolled = CourseEnrollment.objects.filter(
        student=request.user,
        course=exam.course,
        is_active=True
    ).exists()
    
    if not is_enrolled:
        messages.error(request, f'You are not enrolled in the {exam.course.name} course.')
        return redirect('core:dashboard')
    
    # Check if student has already attempted this exam
    existing_attempt = ExamAttempt.objects.filter(
        student=request.user, 
        exam=exam
    ).first()
    
    if existing_attempt:
        messages.error(request, 'You have already attempted this exam.')
        return redirect('core:dashboard')
    
    # Get all questions for this exam
    all_questions = list(exam.questions.all())
    
    # Randomly select questions based on questions_to_display
    if len(all_questions) <= exam.questions_to_display:
        selected_questions = all_questions
    else:
        selected_questions = random.sample(all_questions, exam.questions_to_display)
    
    # Create new attempt
    attempt = ExamAttempt.objects.create(
        student=request.user,
        exam=exam,
        total_questions=len(selected_questions)
    )
    
    # Add selected questions to the attempt
    attempt.selected_questions.set(selected_questions)
    
    messages.success(request, f'Exam "{exam.title}" started! Good luck!')
    return redirect('exams:take_exam', attempt_id=attempt.id)

@login_required
def take_exam(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, student=request.user)
    
    if attempt.status != 'in_progress':
        messages.error(request, 'This exam attempt is no longer active.')
        return redirect('core:dashboard')
    
    # Check if exam time has expired
    elapsed_time = timezone.now() - attempt.start_time
    if elapsed_time.total_seconds() / 60 > attempt.exam.duration_minutes:
        attempt.status = 'timeout'
        attempt.end_time = timezone.now()
        attempt.time_taken_minutes = attempt.exam.duration_minutes
        attempt.save()
        messages.error(request, 'Time is up! Exam has been automatically submitted.')
        return redirect('exams:exam_result', attempt_id=attempt.id)
    
    # Get questions for this attempt (the ones that were randomly selected)
    questions = list(attempt.selected_questions.all())
    if attempt.exam.randomize_questions:
        random.shuffle(questions)
    
    # Get existing answers
    existing_answers = {
        answer.question.id: answer.selected_answer 
        for answer in attempt.answers.all()
    }
    
    remaining_time = attempt.exam.duration_minutes * 60 - elapsed_time.total_seconds()
    
    context = {
        'attempt': attempt,
        'questions': questions,
        'existing_answers': existing_answers,
        'remaining_time': max(0, remaining_time),
        'total_questions': len(questions)
    }
    
    return render(request, 'exams/take_exam.html', context)

@login_required
@require_POST
@csrf_exempt
def submit_exam(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, student=request.user)
    
    if attempt.status != 'in_progress':
        return JsonResponse({'error': 'Exam is not in progress'}, status=400)
    
    try:
        data = json.loads(request.body)
        answers = data.get('answers', {})
        
        # Save answers
        correct_count = 0
        total_score = 0
        
        for question_id, selected_answer in answers.items():
            question = Question.objects.get(id=question_id)
            
            # Delete existing answer if any
            StudentAnswer.objects.filter(
                attempt=attempt, 
                question=question
            ).delete()
            
            # Create new answer
            student_answer = StudentAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_answer=selected_answer
            )
            
            if student_answer.is_correct:
                correct_count += 1
                total_score += question.marks
        
        # Update attempt
        attempt.status = 'completed'
        attempt.end_time = timezone.now()
        attempt.correct_answers = correct_count
        attempt.score = total_score
        
        elapsed_time = attempt.end_time - attempt.start_time
        attempt.time_taken_minutes = int(elapsed_time.total_seconds() / 60)
        attempt.save()
        
        # Send result email
        send_result_email(attempt)
        
        return JsonResponse({
            'success': True,
            'redirect_url': f'/exams/{attempt.id}/result/'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def exam_result(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, student=request.user)
    
    if attempt.status == 'in_progress':
        messages.error(request, 'Exam is still in progress.')
        return redirect('exams:take_exam', attempt_id=attempt.id)
    
    # Get detailed answers
    answers = attempt.answers.select_related('question').order_by('answered_at')
    
    # Calculate percentage
    percentage = (attempt.score / attempt.exam.total_marks * 100) if attempt.exam.total_marks > 0 else 0
    
    context = {
        'attempt': attempt,
        'answers': answers,
        'percentage': round(percentage, 2)
    }
    
    return render(request, 'exams/exam_result.html', context)

def send_result_email(attempt):
    """Send exam result to student's email"""
    try:
        subject = f'Exam Result: {attempt.exam.title}'
        percentage = (attempt.score / attempt.exam.total_marks * 100) if attempt.exam.total_marks > 0 else 0
        
        message = f"""
Dear {attempt.student.first_name},

Your exam results for "{attempt.exam.title}" are ready!

Exam Details:
- Subject: {attempt.exam.subject.name}
- Duration: {attempt.exam.duration_minutes} minutes
- Time Taken: {attempt.time_taken_minutes} minutes

Your Results:
- Score: {attempt.score} out of {attempt.exam.total_marks}
- Correct Answers: {attempt.correct_answers} out of {attempt.total_questions}
- Percentage: {percentage:.2f}%

Thank you for taking the exam!

Best regards,
CBT System Team
"""
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [attempt.student.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Email sending failed: {e}")
