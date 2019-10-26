from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict

from database.models import *
from datetime import date
from django.db.models import Q, F, Sum
from django.db import connection

USERNAME = 'HPRYNNE'
#USERNAME = 'HI'
TODAY = date.today()

def index(request):
    return HttpResponse("At db.")

def employee(request):
    e = Employee()
    e.odin_username = USERNAME
    e = get_employee_id(e)
    if (not e.employee_id):
        return HttpResponse("Invalid username.")
    e = hit_spriden(e)
    e = get_hire_date(e)
    if not e.hire_date:
        return HttpResponse("You are currently not an active employee.")
    e = get_lookback_hrs(e)
    e = get_emails(e)
    e = get_fte(e)
    e = determine_leave_eligibility(e)
    e = get_deductions_info(e)
    e = get_protected_leave_hrs_taken(e)
    e = get_potential_paid_leaves_balances(e)
    return JsonResponse(model_to_dict(e))

def get_employee_id(e: Employee):
    gobeacc_user = gobeacc.objects.filter(gobeacc_username=USERNAME)
    if gobeacc_user:
        e.employee_id = gobeacc_user[0].id
    return e


def hit_spriden(e: Employee):
    spriden_user = spriden.objects.filter(id=e.employee_id)
    if spriden_user:
        e.psu_id = spriden_user[0].id
        e.first_name = spriden_user[0].spriden_first_name
        e.last_name = spriden_user[0].spriden_last_name
    return e

def get_hire_date(e: Employee):
    pebempl_user = pebempl.objects.filter(id=e.employee_id, pebempl_empl_status = 'A')
    # if no hire date, that means they're not active right now
    if pebempl_user:
        e.hire_date=pebempl_user[0].pebempl_first_hire_date
    return e

##TODO: error handling for len is less than 12 and 6 months
def get_lookback_hrs(e: Employee):
    pay_info = perjtot.objects.filter(perjtot_pidm = e.employee_id).filter(Q(perjtot_year = TODAY.year) | Q(perjtot_year = TODAY.year-1))
    ptrearn_eligible = ptrearn.objects.filter(ptrearn_fmla_eligible_hrs_ind='Y')
    pay_info = pay_info.filter(perjtot_earn_code__in=ptrearn_eligible)
    num = pay_info.count()
    pay_info = pay_info[num-12:num]
    e.month_lookback_12 = pay_info.aggregate(Sum('perjtot_hrs')).get('perjtot_hrs__sum')
    num = pay_info.count()
    pay_info2 = pay_info[num-6:num]
    e.month_lookback_6 = pay_info2.aggregate(Sum('perjtot_hrs')).get('perjtot_hrs__sum')
    return e

def get_emails(e: Employee):
    emails = list(goremal.objects.filter(goremal_id=e.employee_id).values_list('goremal_email_address', flat=True))
    e.email = emails
    return e

def get_fte(e: Employee):
    nbrjobs_user = nbrjobs.objects.filter(nbrjobs_pidm=e.employee_id)
    nbrbjob_user = nbrbjob.objects.filter(nbrbjob_pidm=e.employee_id).filter(nbrbjob_end_date__isnull=True)
    if (nbrbjob_user):
        for n in nbrbjob_user:
            positions = nbrjobs_user.filter(nbrjobs_posn=n.nbrbjob_posn).filter(nbrjobs_suff=n.nbrbjob_suff).exclude(Q(nbrjobs_ecls_code='XA') | Q(nbrjobs_ecls_code='XB') | Q(nbrjobs_ecls_code='XC')).values_list('nbrjobs_appt_pct').distinct()
            if (positions):
                e.fte = max(max(positions))
    return e

def determine_leave_eligibility(e: Employee):
    if not e.fte:
        e.fmla_eligibility = 'F' #not eligible
        e.ofla_eligibility = 'F'
        return e
    len = (TODAY - e.hire_date).days / 30
    if (len >= 12  and e.month_lookback_12 >= 1250):
        e.fmla_eligibility = 'T' #eligible
    else:
        e.fmla_eligibility = 'F'
    if (len < 6):
        e.ofla_eligibility = 'M' #military leave only
        return e
    if (e.month_lookback_6 >= 650):
        e.ofla_eligibility = 'T'
        return e
    elif (e.month_lookback_6 >= 520):
        e.ofla_eligibility = 'B' #both military and parental leave
    else:
        e.ofla_eligibility = 'P' #Parental leave only
    return e

def get_deductions_info(e: Employee):
    # stuff like short term disibility etc.
    deductions_info = []
    deductions_info = list(pdrdedn.objects.filter(pdrdedn_pidm=e.employee_id).filter(pdrdedn_status='A').values_list('pdrdedn_bdca_code', flat=True))
    # determine AAUP eligibility
    perbfml_id = perbfml.objects.filter(perbfml_pidm=e.employee_id)[0].perbfml_id
    gorsdav_value = gorsdav.objects.filter(gorsdav_pk_parenttab__contains=perbfml_id).values_list('gorsdav_value')[0].gorsdav_value
    if (gorsdav_value == 'y'):
        deductions_info.append('AAUP')
    e.deductions_eligibility = deductions_info
    print(e.deductions_eligibility)
    return e

def get_protected_leave_hrs_taken(e: Employee):
    ## TODO: figure out when we get there
    anniversary = date.fromisoformat(str(e.hire_date))
    if (TODAY.month > anniversary.month) and (TODAY.month <= 12):
        anniversary.replace(year=TODAY.year)
    elif (TODAY.month < anniversary.month) and (anniversary.month <= 12):
        anniversary.replace(year=TODAY.year-1)
    elif TODAY.month == anniversary.month:
        if TODAY.day >= anniversary.day:
            anniversary.replace(year=TODAY.year)
        else:
            anniversary.replace(year=TODAY.year-1)
    perbfml_id = perbfml.objects.filter(perbfml_pidm=e.employee_id)[0].perbfml_id
    perfmla_id_list = perfmla.objects.filter(perfmla_perbfml_id=perbfml_id).filter(perfmla_begin_date__gte=anniversary).values_list('perfmla_id')
    hrs_claimed = 0
    for p in perfmla_id_list:
        hrs_claimed += perefml.objects.filter(p=perefml_id).values_list('perefml_claim_units')
    e.protected_leave_hrs_taken = hrs_claimed

def get_potential_paid_leaves_balances(e: Employee):
    # current paid leave balances
    perleav_balances = perleav.objects.filter(perleav_pidm=e.employee_id).annotate(current_leave_total=F('perleav_begin_balance') + F('perleav_accrued') - F('perleav_taken')).values_list('perleav_leave_code', 'current_leave_total')
    # accrued paid leave Leave_balances
    phraccr_leav_codes = phraccr.objects.filter(phraccr_pidm=e.employee_id).values_list('phraccr_leav_code', flat=True).distinct()
    phraccr_balances = []
    for p in phraccr_leav_codes:
        result = phraccr.objects.filter(phraccr_pidm=e.employee_id).filter(phraccr_leav_code=p).latest('phraccr_activity_date')
        balance = 0
        if result:
            balance = result.phraccr_curr_accr
        phraccr_balances.append((p, balance))
    # potential paid leave Leave_balances
    paid_leave_balances = []
    # for all of the accrued balances for each leave type, add them to the total of that leave type
    for accrued in phraccr_balances:
        pl_found = False
        for pl in paid_leave_balances:
            if pl[0] == accrued[0]:
                pl[1]+=accrued[1]
                pl_found = True
        if not pl_found:
            paid_leave_balances.append([accrued[0], accrued[1]])
    # for all of the current balances for each leave type, add them to the total of that leave type
    for current in perleav_balances:
        pl_found = False
        for pl in paid_leave_balances:
            if pl[0] == current[0]:
                pl[1]+=current[1]
                pl_found = True
        if not pl_found:
            paid_leave_balances.append([current[0], current[1]])
    with connection.cursor() as cursor:
        cursor.execute("CREATE TEMPORARY TABLE paid_leave_table (leave_code varchar(4) NOT NULL, balance decimal NULL);")
        for p in paid_leave_balances:
            cursor.execute("INSERT into paid_leave_table (leave_code, balance) values (%s, %s);", [p[0], p[1]])
        cursor.execute("SELECT * FROM paid_leave_table;")
        e.paid_leave_balances = cursor.fetchall()
    return e
