from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from database.models import *

import json

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
def save_new_graph(request):
    # TODO: get graph Json blob and name
    #print(request.POST.get('GRAPH_DATA', False))
    new_graph = graph.objects.create(graph_data=request.POST.get('GRAPH_DATA', False), graph_name=request.POST.get('GRAPH_NAME', False), graph_cords=request.POST.get('CORDS', False))

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

@csrf_exempt
def save_new_report(request):
    # TODO: get report Json blob and employee id
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    # print(request.body)
    # print(body.get('EMPLOYEE_ID'))
    # print(body.get('REPORT'))
    new_report = leavereports.objects.create(leavereports_pidm=body.get('EMPLOYEE_ID'), leavereports_report=body.get('REPORT'))
    return HttpResponse("Report received.")

def update_existing_report(request):
    # TODO: get report Json blob and report id and employee id
    report, created = leavereports.update_or_create(
        id=REPORT_ID, defaults={'leavereports_report': REPORT_DATA, 'leavereports_pidm': EMPLOYEE_ID}
    )
