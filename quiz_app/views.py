from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,logout
from django.utils import timezone
from django.http import JsonResponse
from .models import Quiz, Question, UserResponse, CustomUser
from .forms import RegistrationForm, QuizForm
import time

def home_view(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form =  RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz_list')
        else:
            form = RegistrationForm()
        return render(request, 'register.html', {'form': form})
    
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    request.session['quiz_id'] = quiz.id
    request.session['question_index'] = 0
    request.session['start_time'] = time.time()
    request.session['score'] = 0
    request.session['responses'] = []
    return redirect('show_question')

def show_question(request):
    quiz_id = request.session.get('quiz_id')
    question_index = request.session.get('question_index', 0)

    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all().order_by('id')

    if question_index >= len(questions):
        return redirect('quiz_results')

    question = questions[question_index]
    form = QuizForm(question=question)

    if request.method == 'POST':
        form = QuizForm(request.POST, question=question)
        action = request.POST.get('action')

        if form.is_valid():
            selected_option = int(form.cleaned_data['options'])
            is_correct = (selected_option == question.correct_option)

            # Save to database
            UserResponse.objects.create(
                # user=request.user,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct
            )

            # # Store response in session
            responses = request.session.get('responses', [])
            responses.append({
                'question_id': question.id,
                'selected_option': selected_option,
                'is_correct': is_correct
            })
            request.session['responses'] = responses

            # Update score
            if is_correct:
                request.session['score'] = request.session.get('score', 0) + 1

        request.session['question_index'] = question_index + 1
        return redirect('show_question')

    # After you get questions and question_index
    is_last_question = (question_index == len(questions) - 1)

    return render(request, 'question.html', {
        'question': question,
        'form': form,
        'time_limit': question.time_limit,
        'is_last_question': is_last_question,
    })

def quiz_results(request):
    quiz_id = request.session.get('quiz_id')
    if not quiz_id:
        return redirect('quiz_list')
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all().order_by('id')
    responses = request.session.get('responses', [])
    
    # Calculate score from stored answers
    score = 0
    answers = {}
    for response in responses:
        answers[str(response['question_id'])] = response['selected_option']
        question = quiz.question_set.get(id=response['question_id'])
        if response['selected_option'] == question.correct_option:
            score += 1
    
    total_questions = len(questions)
    percentage = round((score / total_questions) * 100) if total_questions > 0 else 0

    # Render the template FIRST before clearing session data
    response = render(request, 'results.html', {
        'quiz': quiz,
        'score': score,
        'total_questions': total_questions,
        'percentage': percentage,
        'answers': answers,
        'responses': responses,
        'questions': questions,
    })
    
    # Clear session quiz data AFTER rendering
    session_keys = ['quiz_id', 'question_index', 'responses', 'score']
    for key in session_keys:
        if key in request.session:
            del request.session[key]

    return response