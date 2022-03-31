from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    # path('eval', views.evaluation, name='eval'),
    path('saveSession', views.saveSession, name='saveSession'),
    path('saveData', views.saveData, name='saveData'),
    path('saveTask', views.saveTask, name='saveTask'),
    path('saveQuestionnaire', views.saveQuestionnaire, name='saveQuestionnaire'),
    path('deleteData', views.deleteData, name='deleteData'),
    path('saveTextInput', views.saveTextInput, name='saveTextInput'),
    path('getScore', views.getScore, name='getScore')
]
