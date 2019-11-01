from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from database.models import *

USERNAME = 'ADENT'

def index(request):
    return HttpResponse("At db.")

def employee(request):
    e = Employee()
    e.set_username(USERNAME)
    e.query_employee_id()
    if (not e.get_employee_id()):
        return HttpResponse("Invalid username.")
    e.query_spriden()
    e.query_hire_date()
    if not e.get_hire_date():
        return HttpResponse("You are currently not an active employee.")
    e.query_other_employee_info()
    return JsonResponse(model_to_dict(e))
