from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from database.models import *


def index(request):
    return HttpResponse("At db.")

#This view creates a request to the employee table with the given employee
#username. It will return a JSON object with all the information regarding a
#particular employee. The purpose of this is to pass that JSON string along to the
#rest of the functionality of the app so that it can use that information to make
#important decisions using the dynamin logic in the application.

@csrf_exempt
def employee(request, usrname):
    e = Employee()
    e.set_username(usrname);
    e.query_employee_id()
    e.query_spriden()
    e.query_hire_date()
    #Checks to make sure the employee is active
    if not e.get_hire_date():
        e.set_fmla_eligibility('F')
        e.set_ofla_eligibility('F')
        return JsonResponse(model_to_dict(e))
    e.query_other_employee_info()
    if not e.get_fte():
        e.set_fmla_eligibility('F')
        e.set_ofla_eligibility('F')
        return JsonResponse(model_to_dict(e))
    return JsonResponse(model_to_dict(e))

@csrf_exempt
def getGraphs(request):
    graphs = query_all_graphs()
    return JsonResponse(graphs, safe=False)
'''
    graph_name = models.CharField(max_length=200, default=str(id))
    graph_date = models.DateField(auto_now=True)
    date = models.DateField(auto_now=True)
    graph_data = jsonfield.JSONField(null=True)
    graph_cords =  models.TextField(default=0)
    #graph_nodes = models.TextField(null=True)
    # 'D' means dormat, 'A' means active
    graph_status = models.CharField(max_length=1, primary_key=True, default='D')
'''
@csrf_exempt
def save_new_graph(request, GRAPH_DATA, GRAPH_NAME, CORDS):
    # TODO: get graph Json blob and name
    new_graph = graph.objects.create(graph_data=GRAPH_DATA, graph_name=GRAPH_NAME, graph_cords = CORDS)

def update_existing_graph(request):
    # TODO: get graph Json blob and id
    graph, created = graph.objects.update_or_create(
        id=GRAPH_ID, defaults={'graph_data': GRAPH_DATA},
    )

def make_graph_active(request):
    # TODO: get graph id
    graph_to_activate, created = graph.objects.get_or_create(
        id=GRAPH_ID, defaults=None,
    )
    graph_to_activate.make_active()

def save_new_report(request):
    # TODO: get report Json blob and employee id
    new_report = leaveReports.objects.create(leavereports_pidm=EMPLOYEE_ID, leavereports_report=REPORT)

def update_existing_report(request):
    # TODO: get report Json blob and report id and employee id
    report, created = leavereports.update_or_create(
        id=REPORT_ID, defaults={'leavereports_report': REPORT_DATA, 'leavereports_pidm': EMPLOYEE_ID}
    )
