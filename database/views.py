from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from database.models import *
import json
import requests

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
    #Checks to see if they are a qualified employee type
    if not e.get_fte():
        e.set_fmla_eligibility('F')
        e.set_ofla_eligibility('F')
        return JsonResponse(model_to_dict(e))
    return JsonResponse(model_to_dict(e))

@csrf_exempt
def get_graphs(request):
    graphs = query_all_graphs()
    return JsonResponse(graphs, safe=False)

@csrf_exempt
def get_active_graph(request):
    graph = query_active_graph()
    return JsonResponse(graph, safe=False)

@csrf_exempt
def save_new_graph(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    #if body:
    new_graph = graph.objects.create(graph_data=body.get('GRAPH_DATA'), graph_cords=body.get('CORDS'))
    return HttpResponse("200")

@csrf_exempt
def update_existing_graph(request):
    # TODO: maybe check if exist, and prompt for graph name if it doesn't and then save
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if body:
        graph, created = graph.objects.update_or_create(
            id=body.get('GRAPH_ID'), defaults={'graph_data': body.get('GRAPH_DATA'), graph_cords: body.get('CORDS'), graph_status: body.get('GRAPH_STATUS')},
        )

@csrf_exempt
def make_graph_active(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if body:
        print("ID: ", body.get('GRAPH_ID'))
        graph_to_activate, created = graph.objects.get_or_create(
            id=body.get('GRAPH_ID'), defaults={'graph_data': body.get('GRAPH_DATA'), 'graph_cords': body.get('CORDS')},
        )
        print(graph_to_activate)
        graph_to_activate.make_active()
        return HttpResponse("200")
    return HttpResponse("400")

@csrf_exempt
def save_new_report(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    #if body:
    new_report = graph.objects.create(leavereports_pidm=body.get('EMPLOYEE_ID'), leavereports_report=body.get('REPORT'))
    return new_report

@csrf_exempt
def update_existing_report(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if body:
        report, created = leavereports.update_or_create(
            id=body.get('REPORT_ID'), defaults={'leavereports_report': body.get('REPORT_DATA'), 'leavereports_pidm': body.get('EMPLOYEE_ID')}
        )
