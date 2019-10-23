from django.shortcuts import render
from django.http import HttpResponse

from database.models import *
from datetime import date
from django.db.models import Q, F, Sum


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
    #employee = JSON.dump(e)
    #return HttpResponse(employee)
    response = hit_spriden(e)
    return HttpResponse(response)

def get_employee_id(e: Employee):
    gobeacc_user = gobeacc.objects.filter(gobeacc_username=USERNAME)
    if gobeacc_user:
        e.employee_id = gobeacc_user[0].id
    return e


def hit_spriden(e: Employee):
    spriden_user = spriden.objects.filter(spriden_id=e.employee_id)
    if not spriden_user:
        return "not found"
    e.psu_id = spriden_user[0].spriden_id
    e.first_name = spriden_user[0].spriden_first_name
    e.last_name = spriden_user[0].spriden_last_name
    return e
'''
def get_hire_date(e: Employee):
    pebempl_user = pebempl.objects.filter(id=e.employee_id, pebempl_empl_status = 'A')
    e.hire_date=pebempl_user[0].pebempl_first_hire_date

def get_lookback_hrs(e: Employee):
    pay_info = perjtot.objects.filter(perjtot_pidm = e.employee_id).filter(Q(perjtot_year = TODAY.year) | Q(perjtot_year = TODAY.year-1))
    ptrearn_eligible = ptrearn.objects.filter(ptrearn_fmla_eligible_hrs_ind='Y')
    pay_info = pay_info.filter(perjtot_earn_code__in=ptrearn_eligible)
    num = pay_info.count()
    pay_info = pay_info[num-12:num]
    e.month_lookback_12 = pay_info.aggregate(Sum('perjtot_hrs'))
    num = pay_info.count()
    pay_info2 = pay_info[num-6:num]
    e.month_lookback_6 = pay_info2.aggregate(Sum('perjtot_hrs'))

def get_emails(e: Employee):
    emails = list(goremal.objects.filter(goremal_id=e.employee_id).values_list('goremal_email_address', flat=True))
    e.email = emails

def get_fte(e: Employee):
    nbrjobs_user = nbrjobs.objects.filter(nbrjobs_pidm=e.employee_id)
    nbrbjob_user = nbrbjob.objects.filter(nbrbjob_pidm=e.employee_id).filter(nbrbjob_end_date__isnull=True)
    if (nbrbjob_user):
        for n in nbrbjob_user:
            positions = nbrjobs_user.filter(nbrjobs_posn=n.nbrbjob_posn).filter(nbrjobs_suff=n.nbrbjob_suff).exclude(Q(nbrjobs_ecls_code='XA') | Q(nbrjobs_ecls_code='XB') | Q(nbrjobs_ecls_code='XC')).values_list('nbrjobs_appt_pct').distinct()
            if (positions):
                e.fte = max(max(positions))

def determine_leave_eligibility(e: Employee):
    if (e.fte == null):
        e.fmla_eligibility = 'F' #not eligible
        e.ofla_eligibility = 'F'
        return
    len = (TODAY - e.hire_date).days / 30
    if (len >= 12  and e.month_lookback_12 >= 1250):
        e.fmla_eligibility = 'T' #eligible
    else:
        e.fmla_eligibility = 'F'
    if (len < 6):
        e.ofla_eligibility = 'M' #military leave only
        return
    if (e.month_lookback_6 >= 650):
        e.ofla_eligibility = 'T'
        return
    elif (e.month_lookback_6 >= 520):
        e.ofla_eligibility = 'B' #both military and parental leave
    else:
        e.ofla_eligibility = 'P' #Parental leave only

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
'''
#def get_leftover_protected_leave_balances(e: Employee):
    ## TODO: figure out when we get there
'''
    Leftover protected leave balances = perbfml_max_units - perefml_claim_units (for each perefml_earn_code)

    perfmla_ids = perbfmla.objects.filter(perfmla_perbfml_id = perbfml_id).filter(perfmla_begin_date.year = TODAY.year).values_list('perfmla_id')
    For all P in perfmla_ids:
	   p_unit = perefml.objects.filter(p = perefml_id).values_list('perefml_claim_units')
	   claim_units+=p_unit
	e.max_protected_leave_hrs = (eligible time based on eligible leave type)( e.fte/100)
    protected_leave_balance = e.max_protected_leave_hrs - claim_units
'''

#def get_potential_paid_leaves_balances(e: Employee):
    # current paid leave balances
    # # TODO: test --> perleav_balances = perleav.objects.filter(perleav_pidm=e.employee_id).annotate(current_leave_total=F('perleav_begin_balance') + F('perleav_accrued') - F('perleav_taken')).values('perleav_leave_code', 'current_leave_total')
    # accrued paid leave Leave_balances
    # # TODO: test --> phraccr_balances = phraccr.objects.filter(phraccr_pidm=e.employee_id).filter(Q(phraccr_activity_date.month = TODAY.month) & Q(phraccr_activity_date.year = TODAY.year)).values_list('phraccr_leav_code', 'phraccr_curr_accr')
    # potential paid leave Leave_balances
    # paid_leave_balances = [{leave_code, balance}]
'''
    for p in paid_leave_balances:
        for a in phraccr_balances:
            if (a.phraccr_leav_code == p.leave_code):
                p.balance+=a.phraccr_curr_accr
        for c in perleav_balances:
            if (c.perleav_leave_code == p.leave_code):
                p.balance+=c.current_leave_total
'''
    ## TODO: store somewhere
