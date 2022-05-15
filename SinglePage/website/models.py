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
    study = models.ManyToManyField(Study, related_name='tasks')

    def __str__(self):
        return self.name


# Tasks
class Task(models.Model):
    description = models.CharField(max_length=200)
    details = models.CharField(max_length=20, default="", blank=True)
    item = models.CharField(max_length=200, default="", blank=True)
    task_set = models.ForeignKey(TaskSet, on_delete=models.CASCADE)
    image_link = models.CharField(max_length=200, default="", blank=True)

    def __int__(self):
        return self.pk


# Task Answer Choices
class AnswerChoice(models.Model):
    text = models.CharField(max_length=200, default="", blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.text


# -------------------------------------------------------------


## Questionnaires
# Questionnaire Types
class Questionnaire(models.Model):
    name = models.CharField(max_length=128)
    study = models.ManyToManyField(Study, related_name='questionnaires')

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
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    list_p1 = models.CharField(max_length=128)
    list_p2 = models.CharField(max_length=128)
    list_m1 = models.CharField(max_length=128)
    list_m2 = models.CharField(max_length=128)
    terms_agree = models.BooleanField(default=False)
    age = models.TextField(max_length=25, null=True)
    framing = models.IntegerField(null=True)
    gender = models.CharField(max_length=100, null=True)
    finished = models.BooleanField(default=False)
    suspect_deception = models.BooleanField(null=True)
    text_deception = models.TextField(null=True, blank=True)
    request_delete = models.BooleanField(default=False)

    def __int__(self):
        return self.pk


class QuestionnaireSubmission(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)  # pre or main, page 1 or page 2
    item = models.CharField(max_length=20)  # order of task on page
    answer = models.CharField(max_length=20)

    def __int__(self):
        return self.pk


class TaskSubmission(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)  # pre or main, page 1 or page 2
    item = models.CharField(max_length=20)  # order of task on page
    task_id = models.IntegerField()
    answer = models.CharField(max_length=20)

    def __int__(self):
        return self.pk


class TaskScore(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    score_pre = models.IntegerField(default=0)
    score_main = models.IntegerField(default=0)

    def __int__(self):
        return self.pk


class TimeSpend(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    page_nr = models.IntegerField(default=0)
    start_time = models.FloatField()
