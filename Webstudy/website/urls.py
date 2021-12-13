from django.urls import path

from . import views, views_ctrl

urlpatterns = [
    path('', views.index, name='index'),
    # path('redirect', views.redirect, name='redirect'),
    path('index', views.index, name='index'),
    # path('page1', views.page1, name='page1'),
    # path('page2', views.page2, name='page1'),

    path('nextpage', views_ctrl.nextpage, name='nextpage'),
]
