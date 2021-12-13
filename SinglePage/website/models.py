from django.db import models
from django.contrib.sessions.models import Session


class Study(models.Model):
    name = models.CharField(max_length=128, default="")

    def __str__(self):
        return self.name


class Questionnaire(models.Model):
    name = models.CharField(max_length=128)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Question(models.Model):
    answer = models.CharField(max_length=128)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer
