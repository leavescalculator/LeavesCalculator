from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('savegraph/', views.save_new_graph, name='savegraph'),
    path('savereport/', views.save_new_report, name='savereport'),
    path('<str:usrname>/', views.employee, name='employee'),
    path('employee/', views.employee, name='employee')
]
