from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['options'] = forms.ChoiceField(
            choices=[
                (1, question.option1),
                (2, question.option2),
                (3, question.option3),
                (4, question.option4),
            ],
            widget=forms.RadioSelect
        )


