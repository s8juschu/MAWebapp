from django.contrib import admin

# Register your models here.
from .models import Study, TaskSet, Task, Answer, Questionnaire, Question, AnswerChoice


class TaskSetAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'study')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'description', 'text', 'task_set', 'image_link')


class AnswerChoiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'answer')


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'study')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'questionnaire')


# class ChoiceAdmin(admin.ModelAdmin):
#     list_display = ('answer', 'question', 'session')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'answer', 'question_nr', 'session', 'task')


admin.site.register(Study)
admin.site.register(TaskSet, TaskSetAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(AnswerChoice, AnswerChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice, ChoiceAdmin)
