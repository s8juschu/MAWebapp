from django.contrib import admin
from django.contrib.sessions.models import Session

# Register your models here.
from .models import Study, TaskSet, Task, Submission, QuestionnaireSubmission, TaskSubmission, Questionnaire,\
    Question, AnswerChoice, TaskScore, TimeSpend


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


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
    list_display = ('pk', 'text', 'task', 'correct_answer')


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'get_study')

    def get_study(self, obj):
        return obj.study.all()


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'questionnaire')


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'study', 'session', 'framing', 'age', 'gender', 'list_p1', 'list_p2', 'list_m1',
                    'list_m2', 'terms_agree', 'finished', 'suspect_deception', 'text_deception', 'request_delete')


class QuestionnaireSubmissionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'session', 'submission', 'name', 'type', 'item', 'question_id', 'answer')


class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'session', 'submission', 'type', 'item', 'task_id', 'answer')


class TaskScoreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'session', 'submission', 'score_pre', 'score_main')


class TimeSpendAdmin(admin.ModelAdmin):
    list_display = ('pk', 'session', 'submission', 'page_nr', 'start_time')


admin.site.register(Session, SessionAdmin)
admin.site.register(Study)
admin.site.register(TaskSet, TaskSetAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(AnswerChoice, AnswerChoiceAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(QuestionnaireSubmission, QuestionnaireSubmissionAdmin)
admin.site.register(TaskSubmission, TaskSubmissionAdmin)
admin.site.register(TaskScore, TaskScoreAdmin)
admin.site.register(TimeSpend, TimeSpendAdmin)
