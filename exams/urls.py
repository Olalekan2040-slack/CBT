from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('list/', views.exam_list, name='exam_list'),
    path('<uuid:attempt_id>/take/', views.take_exam, name='take_exam'),
    path('<uuid:attempt_id>/submit/', views.submit_exam, name='submit_exam'),
    path('<uuid:attempt_id>/result/', views.exam_result, name='exam_result'),
    path('start/<int:exam_id>/', views.start_exam, name='start_exam'),
]
