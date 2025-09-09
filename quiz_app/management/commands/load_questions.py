import json
from django.core.management.base import BaseCommand
from quiz_app.models import Question, Quiz

class Command(BaseCommand):
    help = 'Load questions from JSON file'

    def handle(self, *args, **options):
        with open('questions.json') as f:
            questions = json.load(f)
            for q in questions:
                quiz = Quiz.objects.get(id=q['quiz_id'])
                Question.objects.create(
                    quiz=quiz,
                    text=q['text'],
                    option1=q['option1'],
                    option2=q['option2'],
                    option3=q['option3'],
                    option4=q['option4'],
                    correct_option=q['correct_option']
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded questions!'))