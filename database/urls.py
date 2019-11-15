from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('savegraph/', views.save_new_graph, name='savegraph'),
    path('<str:usrname>/', views.employee, name='employee'),
    path('employee/', views.employee, name='employee')
]
