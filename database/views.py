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

'''
Output:

{
    "employee_id": 800009,
    "odin_username": "HPRYNNE",
    "psu_id": "953125510",
    "first_name": "Hester",
    "last_name": "Prynne",
    "email": [
        "leaves@pdx.edu",
        "hrc-tech-team-group@pdx.edu"
    ],
    "hire_date": "2006-03-20",
    "fte": 1.0,
    "month_lookback_12": "1711.48000000000",
    "month_lookback_6": "833.75",
    "fmla_eligibility": "T",
    "ofla_eligibility": "T",
    "deductions_eligibility": [
        "LST",
        "LTD",
        "PXS"
    ],
    "paid_leave_balances": [
        [
            "XBRV",
            0
        ],
        [
            "ASIC",
            45.91
        ],
        [
            "AVAC",
            116.88
        ],
        [
            "PERS",
            15.5
        ],
        [
            "FLSA",
            0
        ],
        [
            "NFLS",
            0
        ],
        [
            "XCHG",
            0
        ],
        [
            "XOTH",
            0
        ],
        [
            "XFUR",
            0
        ],
        [
            "XDON",
            0
        ]
    ],
    "protected_leave_hrs_taken": 0,
    "max_protected_leave_hrs": null
}
'''
