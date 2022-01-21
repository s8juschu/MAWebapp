from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('eval', views.evaluation, name='eval'),
    path('saveSession', views.saveSession, name='saveSession'),
    path('saveData', views.saveData, name='saveData'),
    path('saveIMI', views.saveIMI, name='saveIMI')
    # path('savePXI', views.savePXI, name='savePXI')
]
