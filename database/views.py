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
        e.set_fmla_eligibility('F')
        e.set_ofla_eligibility('F')
        return JsonResponse(model_to_dict(e))
        #return HttpResponse("Invalid username.")
    e.query_spriden()
    #Checks the hire date to detemine the eligibility of the employee
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
    #graph = Graph()
    #graph.query_graphs()
    #e.graph = model_to_dict(graph)


#def all_graphs(request):
#    graph = Graph()
#    graph.query_graphs()
#    return JsonResponse(model_to_dict(graph))
