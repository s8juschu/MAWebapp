from django.db import models
from django.contrib.sessions.models import Session


class Study(models.Model):
    name = models.CharField(max_length=128, default="")

    def __str__(self):
        return self.name


## Tasks
# Task Types
class TaskSet(models.Model):
    name = models.CharField(max_length=200)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Tasks
class Task(models.Model):
    description = models.CharField(max_length=200)
    text = models.CharField(max_length=200, default="", blank=True)
    task_set = models.ForeignKey(TaskSet, on_delete=models.CASCADE)
    image_link = models.CharField(max_length=200,  default="", blank=True)

    def __int__(self):
        return self.pk


# Task Answer Choices
class AnswerChoice(models.Model):
    text = models.CharField(max_length=200, default="", blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

# -------------------------------------------------------------
# Answer of Tasks
class Answer(models.Model):
    question_nr = models.IntegerField()
    answer = models.CharField(max_length=128)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer
# -------------------------------------------------------------


## Questionnaires
# Questionnaire Types
class Questionnaire(models.Model):
    name = models.CharField(max_length=128)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Question
class Question(models.Model):
    text = models.CharField(max_length=200)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

#
# # Question Options
# class Choice(models.Model):
#     session = models.ForeignKey(Session, on_delete=models.CASCADE)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     answer = models.CharField(max_length=128)
#
#     def __str__(self):
#         return self.choice_text
