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
    details = models.CharField(max_length=20, default="", blank=True)
    text = models.CharField(max_length=200, default="", blank=True)
    task_set = models.ForeignKey(TaskSet, on_delete=models.CASCADE)
    image_link = models.CharField(max_length=200, default="", blank=True)

    def __int__(self):
        return self.pk


# Task Answer Choices
class AnswerChoice(models.Model):
    text = models.CharField(max_length=200, default="", blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


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


# -------------------------------------------------------------


# Answers of Study
class Submission(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer


class GeneralData(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    list_p1 = models.CharField(max_length=128)
    list_p2 = models.CharField(max_length=128)
    list_m1 = models.CharField(max_length=128)
    list_m2 = models.CharField(max_length=128)
    terms_agree = models.BooleanField()
    finished = models.BooleanField()

    def __int__(self):
        return self.pk


class PersonalData(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    age = models.IntegerField()
    nationality = models.CharField(max_length=128)
    gender = models.CharField(max_length=20)

    def __int__(self):
        return self.pk


class QuestionnaireSubmission(models.Model):
    submission = models.ManyToManyField(Submission)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    description = models.CharField(max_length=20)  # pre or main

    def __int__(self):
        return self.pk


class TaskSubmission(models.Model):
    submission = models.ManyToManyField(Submission)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    task_id = models.IntegerField()
    answer = models.CharField(max_length=20)

    def __int__(self):
        return self.pk
