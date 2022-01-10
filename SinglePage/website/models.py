from django.db import models
from django.contrib.sessions.models import Session


class Study(models.Model):
    name = models.CharField(max_length=128, default="")

    def __str__(self):
        return self.name


## Aufgaben
# Aufgabensatz
class TaskSet(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Aufgabe
class Task(models.Model):
    task_text = models.CharField(max_length=200)
    task_set = models.ForeignKey(TaskSet, on_delete=models.CASCADE)
    image_link = models.CharField(max_length=200,  default="", blank=True)

    def __str__(self):
        return self.task_text


# Antwort der Aufgabe
class Answer(models.Model):
    question_nr = models.IntegerField()
    answer = models.CharField(max_length=128)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer


## Fragebögen
# Fragebogensatz
class Questionnaire(models.Model):
    name = models.CharField(max_length=128)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Frage
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


# Antwort
class Choice(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=128)

    def __str__(self):
        return self.choice_text
