from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=True)

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveBigIntegerField(help_text="Duration in minutes")

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    option1 = models.CharField(max_length=100, default="Default Option 1")
    option2 = models.CharField(max_length=100, default="Default Option 2")
    option3 = models.CharField(max_length=100, default="Default Option 3")
    option4 = models.CharField(max_length=100, default="Default Option 4")
    correct_option = models.IntegerField(default=1)
    time_limit = models.PositiveBigIntegerField(default=15, help_text="Time limit in seconds")

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

class UserResponse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.IntegerField(default="1")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
