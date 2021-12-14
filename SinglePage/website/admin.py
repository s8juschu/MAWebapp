from django.contrib import admin

# Register your models here.
from .models import Study, Questionnaire, Question, Answer


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question_nr', 'session', 'study')


admin.site.register(Study)
admin.site.register(Questionnaire)
admin.site.register(Question)
admin.site.register(Answer, AnswerAdmin)
