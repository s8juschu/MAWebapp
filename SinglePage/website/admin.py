from django.contrib import admin

# Register your models here.
from .models import Study, TaskSet, Task, Submission, Questionnaire, Question, AnswerChoice


class TaskSetAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'study')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'description', 'details', 'text', 'task_set', 'image_link')


class AnswerChoiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'task')


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'study')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'questionnaire')


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'session')


admin.site.register(Study)
admin.site.register(TaskSet, TaskSetAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(AnswerChoice, AnswerChoiceAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Submission, SubmissionAdmin)
