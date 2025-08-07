from django.contrib import admin
from django.db.models import Count
from .models import Subject, Question, Exam, ExamQuestion, ExamAttempt, StudentAnswer

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'question_count', 'created_at')
    search_fields = ('name',)
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text_short', 'subject', 'difficulty', 'marks', 'correct_answer', 'created_by', 'created_at')
    list_filter = ('subject', 'difficulty', 'marks', 'created_at')
    search_fields = ('question_text', 'subject__name')
    list_editable = ('difficulty', 'marks')
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class ExamQuestionInline(admin.TabularInline):
    model = ExamQuestion
    extra = 0
    raw_id_fields = ('question',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'duration_minutes', 'questions_to_display', 'total_marks', 'is_active', 'question_count', 'attempt_count')
    list_filter = ('subject', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    inlines = [ExamQuestionInline]
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'
    
    def attempt_count(self, obj):
        return obj.examattempt_set.count()
    attempt_count.short_description = 'Attempts'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'status', 'score', 'correct_answers', 'total_questions', 'time_taken_minutes', 'start_time')
    list_filter = ('status', 'exam', 'start_time')
    search_fields = ('student__email', 'student__first_name', 'student__last_name', 'exam__title')
    readonly_fields = ('id', 'start_time', 'time_taken_minutes')
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation of attempts

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question_short', 'selected_answer', 'is_correct', 'answered_at')
    list_filter = ('is_correct', 'selected_answer', 'answered_at')
    search_fields = ('attempt__student__email', 'question__question_text')
    readonly_fields = ('is_correct', 'answered_at')
    
    def question_short(self, obj):
        return obj.question.question_text[:50] + "..." if len(obj.question.question_text) > 50 else obj.question.question_text
    question_short.short_description = 'Question'
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation of answers
