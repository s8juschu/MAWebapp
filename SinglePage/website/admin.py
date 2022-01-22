from django.contrib import admin

# Register your models here.
from .models import Study, TaskSet, Task, Submission, QuestionnaireSubmission, TaskSubmission, Questionnaire,\
    Question, AnswerChoice


class StudyAdmin (admin.ModelAdmin):
    list_display = ('pk', 'name', 'get_task', 'get_questionnaire')

    def get_task(self, obj):
        return obj.tasks.all()

    def get_questionnaire(self, obj):
        return obj.questionnaires.all()


class TaskSetAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'get_study')

    def get_study(self, obj):
        return obj.study.all()


class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'description', 'details', 'item', 'task_set', 'image_link')


class AnswerChoiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'task')


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'get_study')

    def get_study(self, obj):
        return obj.study.all()


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'questionnaire')


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'study', 'session', 'age', 'nationality', 'gender', 'list_p1', 'list_p2', 'list_m1', 'list_m2',
                    'terms_agree', 'finished')


class QuestionnaireSubmissionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'session', 'submission', 'type', 'questionnaire_id', 'answer')


class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'session', 'submission', 'type', 'item', 'task_id', 'answer')


admin.site.register(Study)
admin.site.register(TaskSet, TaskSetAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(AnswerChoice, AnswerChoiceAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(QuestionnaireSubmission, QuestionnaireSubmissionAdmin)
admin.site.register(TaskSubmission, TaskSubmissionAdmin)
