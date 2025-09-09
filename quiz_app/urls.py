from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register, name='register'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('question/', views.show_question, name='show_question'),
    path('results/', views.quiz_results, name='quiz_results'),
]