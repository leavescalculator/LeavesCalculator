from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('savegraph/', views.save_new_graph, name='savegraph'),
    path('updategraph/', views.update_existing_graph, name='updategraph'),
    path('getgraphs/', views.get_graphs, name='getgraphs'),
    path('activategraph/', views.make_graph_active, name='activategraph'),
    path('savereport/', views.save_new_report, name='savereport'),
    path('updatereport/', views.update_existing_report, name='updatereport'),
    path('<str:usrname>/', views.employee, name='employee'),
    path('employee/', views.employee, name='employee')
]
