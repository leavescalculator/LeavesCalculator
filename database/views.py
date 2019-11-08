from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from database.models import *

USERNAME = 'DBROOKS'


def index(request):
    return HttpResponse("At db.")

#This view creates a request to the employee table with the given employee
#username. It will return a JSON object with all the information regarding a
#particular employee. The purpose of this is to pass that JSON string along to the
#rest of the functionality of the app so that it can use that information to make
#important decisions using the dynamin logic in the application.
def employee(request):
    e = Employee()
    e.set_username(USERNAME)
    e.query_employee_id()
    #If the ID does not exist
    if (not e.get_employee_id()):
        return HttpResponse("Invalid username.")
    e.query_spriden()
    #Checks the hire date to detemine the eligibility of the employee
    e.query_hire_date()
    #Checks to make sure the employee is active
    if not e.get_hire_date():
        return HttpResponse("You are currently not an active employee.")
    e.query_other_employee_info()
    return JsonResponse(model_to_dict(e))

def reports(request):
    reports = leavereports.objects.filter(leavereports_pidm=PIDM).values_list('leavereports_date', 'leavereports_report')

def all_graphs(request):
    graph = graph.objects().all()
