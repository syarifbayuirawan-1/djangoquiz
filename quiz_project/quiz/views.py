from django.shortcuts import render
from .models import Question, Choice
from .forms import QuizForm

def quiz_view(request):
    questions = Question.objects.all()
    incorrect_questions = []  # List for incorrect answers
    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            total_questions = questions.count()
            for question in questions:
                selected_choice_id = form.cleaned_data.get(f'question_{question.id}')
                if selected_choice_id:
                    selected_choice = Choice.objects.get(id=selected_choice_id)
                    if selected_choice.is_correct:
                        score += 1
                    else:
                        incorrect_questions.append(question)
            return render(request, 'quiz/result.html', {
                'score': score,
                'total_questions': total_questions,
                'incorrect_questions': incorrect_questions,
            })
    else:
        form = QuizForm(questions=questions)
    return render(request, 'quiz/quiz.html', {'form': form})
