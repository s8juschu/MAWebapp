from django.contrib import admin

# Register your models here.
from .models import Study, TaskSet, Task, Answer, Questionnaire, Question, AnswerTypes, AnswerChoice


class TaskSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'study')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'text', 'task_set', 'image_link')


class AnswerTypesAdmin(admin.ModelAdmin):
    list_display = ('description', 'task_set')


class AnswerChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'answer_type')


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('name', 'study')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'questionnaire')


# class ChoiceAdmin(admin.ModelAdmin):
#     list_display = ('answer', 'question', 'session')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question_nr', 'session', 'task')


admin.site.register(Study)
admin.site.register(TaskSet, TaskSetAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(AnswerChoice, AnswerChoiceAdmin)
admin.site.register(AnswerTypes, AnswerTypesAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice, ChoiceAdmin)
