from email.policy import default
from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

class Quiz(models.Model):
    q_order = models.IntegerField()
    quiz_body = models.CharField(max_length=300)

    def __str__(self):
        return self.quiz_body

class Choice(models.Model):
    text = models.CharField(max_length=50)
    is_correct = models.BooleanField(default=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    def __str__(self):
        return self.text
