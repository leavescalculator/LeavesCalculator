from django.db import models
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, F, Sum
from django.db import connection
import jsonfield
from django.forms.models import model_to_dict
from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()

TODAY = date.today()


#The following schema was provided by PSU. They also provided mock information
#that's supposed to simulate the information that they store in their own
#database. The purpose of it was to provide a way to test the functinality of
#the application as a whole.

class gobeacc(models.Model):
    id = models.IntegerField(primary_key=True)
    gobeacc_username = models.CharField(max_length=30)

    def _str_(self):
        return self.name

class goremal(models.Model):
    goremal_id = models.IntegerField(default=0)
    goremal_emal_code = models.CharField(max_length=4)
    goremal_email_address = models.CharField(max_length=128)
    def _str_(self):
        return self.name

class gorsdav(models.Model):
    gorsdav_table_name = models.CharField(max_length=30)
    gorsdav_attr_name = models.CharField(max_length=30)
    gorsdav_pk_parenttab = models.CharField(max_length=512)
    gorsdav_value = models.CharField(max_length=1)
    def _str_(self):
        return self.name

class nbrjobs(models.Model):
    nbrjobs_pidm = models.IntegerField(default=0)
    nbrjobs_posn = models.CharField(max_length=6)
    nbrjobs_suff = models.CharField(max_length=2)
    nbrjobs_effective_date = models.DateField()
    nbrjobs_ecls_code = models.CharField(max_length=2)
    nbrjobs_appt_pct = models.IntegerField()
    def _str_(self):
        return self.name

class nbrbjob(models.Model):
    nbrbjob_pidm = models.IntegerField(default=0)
    nbrbjob_posn = models.CharField(max_length=6)
    nbrbjob_suff = models.CharField(max_length=2)
    nbrbjob_contract_type = models.CharField(max_length=1)
    nbrbjob_begin_date = models.DateField(null=True, blank=True)
    nbrbjob_end_date = models.DateField(null=True, blank=True)
    def _str_(self):
        return self.name

class spriden(models.Model):
    id = models.IntegerField(primary_key=True)
    spriden_id = models.CharField(max_length=9)
    spriden_last_name = models.CharField(max_length=60)
    spriden_first_name = models.CharField(max_length=60)
    def _str_(self):
        return self.name

class pebempl(models.Model):
    id = models.IntegerField(primary_key=True)
    pebempl_empl_status = models.CharField(max_length=1)
    pebempl_first_hire_date = models.DateField()
    def _str_(self):
        return self.name

class phraccr(models.Model):
    phraccr_pidm =  models.IntegerField(default=0)
    phraccr_leav_code = models.CharField(max_length=4)
    phraccr_curr_accr = models.IntegerField()
    phraccr_activity_date = models.DateField()
    def _str_(self):
        return self.name

class perleav(models.Model):
    perleav_pidm = models.IntegerField(default=0)
    perleav_leave_code = models.CharField(max_length=4)
    perleav_begin_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    perleav_accrued = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    perleav_taken = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def _str_(self):
        return self.name

class perefml(models.Model):
    id = models.IntegerField(primary_key=True)
    perefml_perbfmla_id = models.IntegerField()
    perefml_earn_code = models.CharField(max_length=3)
    perefml_claim_units = models.IntegerField()
    def _str_(self):
        return self.name

class perfmla(models.Model):
    perfmla_id = models.IntegerField(default=0)
    perfmla_perbfml_id = models.IntegerField()
    perfmla_begin_date = models.DateField();
    def _str_(self):
        return self.name

class perbfml(models.Model):
    perbfml_pidm = models.IntegerField(default=0)
    perbfml_max_units = models.IntegerField(default=0)
    perbfml_id = models.IntegerField(default=0)
    def _str_(self):
        return self.name

class perjtot(models.Model):
    perjtot_pidm = models.IntegerField(default=0)
    perjtot_earn_code = models.CharField(max_length=3)
    perjtot_year = models.IntegerField()
    perjtot_month = models.IntegerField()
    perjtot_hrs = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def _str_(self):
        return self.name

class ptrearn(models.Model):
    id = models.CharField(max_length=3,primary_key=True)
    ptrearn_fmla_eligible_hrs_ind = models.CharField(max_length=1)

class pdrdedn(models.Model):
    pdrdedn_pidm =models.IntegerField()
    pdrdedn_bdca_code = models.CharField(max_length=3)
    pdrdedn_effective_date = models.DateField()
    pdrdedn_status = models.CharField(max_length = 1)
    def _str_(self):
        return self.name

class graph(models.Model):
    graph_name = models.CharField(max_length=200, default=str(id))
    graph_date = models.DateField(auto_now=True)
    date = models.DateField(auto_now=True)
    graph_data = jsonfield.JSONField(null=True)
    graph_cords =  models.TextField(default=0)
    #graph_nodes = models.TextField(null=True)
    # 'D' means dormat, 'A' means active
    graph_status = models.CharField(max_length=1, primary_key=True, default='D')
    def _str_(self):
        return self.name

    def make_active():
        current_active_graph = graph.objects.filter(graph_status='A')
        if current_active_graph:
            current_active_graph.graph_status = 'D'
            current_active_graph.save()
        self.graph_status = 'A'
        self.save()

def query_active_graph():
    active_graph = graph.objects.filter(graph_status='A')
    if active_graph:
        return active_graph[0]

def query_all_graphs():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM database_graph;")
        return dictfetchall(cursor)

class leavereports(models.Model):
    leavereports_pidm = models.IntegerField()
    leavereports_pidm = models.IntegerField(primary_key=True)
    leavereports_date = models.DateField(auto_now=True)
    leavereports_report = jsonfield.JSONField()
    def _str_(self):
        return self.name
# Helper models below

#This function is provided by django tutorials at: https://docs.djangoproject.com/en/2.2/topics/db/sql/
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]

#The employee class queries for all the information stored in the tables regarding one
#particular employee. The employee's request is made with an employee's username. An example
#of this can be observed in views.py.
class Employee(models.Model):
    employee_id  = models.IntegerField(primary_key=True)
    odin_username = models.CharField(max_length=200)
    psu_id = models.IntegerField(default=0)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    hire_date = models.DateField()
    fte = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    employee_classification = models.CharField(max_length=2, default=0.0)
    month_lookback_12 = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    month_lookback_6 = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    fmla_eligibility = models.CharField(max_length=1)
    ofla_eligibility = models.CharField(max_length=1)
    deductions_eligibility = models.CharField(max_length=200)
    paid_leave_balances = models.TextField(default=0)
    protected_leave_hrs_taken = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    max_protected_leave_hrs = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    #reports = jsonfield.JSONField()
    reports = models.TextField(null=True)
    graph = jsonfield.JSONField(null=True)

    def query_employee_id(self):
        gobeacc_user = gobeacc.objects.filter(gobeacc_username=self.odin_username)
        if gobeacc_user:
            self.employee_id = gobeacc_user[0].id

    def query_spriden(self):
        spriden_user = spriden.objects.filter(id=self.employee_id)
        if spriden_user:
            self.psu_id = spriden_user[0].spriden_id
            self.first_name = spriden_user[0].spriden_first_name
            self.last_name = spriden_user[0].spriden_last_name

    def query_hire_date(self):
        pebempl_user = pebempl.objects.filter(id=self.employee_id, pebempl_empl_status = 'A')
        # if no hire date, that means they're not active right now
        if pebempl_user:
            self.hire_date=pebempl_user[0].pebempl_first_hire_date

    def query_lookback_hrs(self):
        pay_info = perjtot.objects.filter(perjtot_pidm = self.employee_id).filter(Q(perjtot_year = TODAY.year) | Q(perjtot_year = TODAY.year-1))
        ptrearn_eligible = ptrearn.objects.filter(ptrearn_fmla_eligible_hrs_ind='Y')
        pay_info = pay_info.filter(perjtot_earn_code__in=ptrearn_eligible)
        num = pay_info.count()
        if num >= 12:
            pay_info = pay_info[num-12:num]
        self.month_lookback_12 = pay_info.aggregate(Sum('perjtot_hrs')).get('perjtot_hrs__sum')
        num = pay_info.count()
        if num >= 6:
            pay_info2 = pay_info[num-6:num]
        self.month_lookback_6 = pay_info2.aggregate(Sum('perjtot_hrs')).get('perjtot_hrs__sum')

    def query_emails(self):
        emails = list(goremal.objects.filter(goremal_id=self.employee_id).distinct().values_list('goremal_email_address', flat=True))
        self.email = emails

    def query_fte_and_classification(self):
        nbrjobs_user = nbrjobs.objects.filter(nbrjobs_pidm=self.employee_id)
        nbrbjob_user = nbrbjob.objects.filter(nbrbjob_pidm=self.employee_id).filter(Q(nbrbjob_begin_date__lte=TODAY) & (Q(nbrbjob_end_date__isnull=True) | Q(nbrbjob_end_date__gt=TODAY)))
        if (nbrbjob_user):
            for n in nbrbjob_user:
                positions = nbrjobs_user.filter(nbrjobs_posn=n.nbrbjob_posn).filter(nbrjobs_suff=n.nbrbjob_suff).exclude(Q(nbrjobs_ecls_code='XA') | Q(nbrjobs_ecls_code='XB') | Q(nbrjobs_ecls_code='XC')).values_list('nbrjobs_appt_pct').distinct()
                if (positions):
                    self.fte = max(max(positions))/100
                    employee_classification = nbrjobs_user.filter(nbrjobs_posn=n.nbrbjob_posn).filter(nbrjobs_suff=n.nbrbjob_suff).values_list('nbrjobs_ecls_code').distinct()
                    if employee_classification:
                        self.employee_classification = employee_classification[0][0]

    def query_leave_eligibility(self):
        if not self.fte:
            self.fmla_eligibility = 'F' #not eligible
            self.ofla_eligibility = 'F'
            return
        len = (TODAY - self.hire_date).days / 30
        if (len >= 12  and self.month_lookback_12 >= 1250):
            self.fmla_eligibility = 'T' #eligible
        else:
            self.fmla_eligibility = 'F'
        if (len < 6):
            self.ofla_eligibility = 'M' #military leave only
            return
        if (self.month_lookback_6 >= 650):
            self.ofla_eligibility = 'T'
            return
        elif (self.month_lookback_6 >= 520):
            self.ofla_eligibility = 'B' #both military and parental leave
        else:
            self.ofla_eligibility = 'P' #Parental leave only
        return self

    def query_deductions_info(self):
        # stuff like short term disibility etc.
        deductions_info = []
        deductions_info = list(pdrdedn.objects.filter(pdrdedn_pidm=self.employee_id).filter(pdrdedn_status='A').values_list('pdrdedn_bdca_code', flat=True))
        # determine AAUP eligibility
        perbfml_obj = perbfml.objects.filter(perbfml_pidm=self.employee_id)
        if perbfml_obj:
            perbfml_id = perbfml_obj[0].perbfml_id
            gorsdav_obj = gorsdav.objects.filter(gorsdav_pk_parenttab__contains=perbfml_id).values_list('gorsdav_value')
            if gorsdav_obj:
                gorsdav_value = gorsdav_obj[0][0]
                if (gorsdav_value == 'y'):
                    deductions_info.append('AAUP')
        self.deductions_eligibility = deductions_info

    def query_protected_leave_hrs_taken(self):
        hrs_claimed = 0
        anniversary = date.fromisoformat(str(self.hire_date))
        if (TODAY.month > anniversary.month) and (TODAY.month <= 12):
            anniversary.replace(year=TODAY.year)
        elif (TODAY.month < anniversary.month) and (anniversary.month <= 12):
            anniversary.replace(year=TODAY.year-1)
        elif TODAY.month == anniversary.month:
            if TODAY.day >= anniversary.day:
                anniversary.replace(year=TODAY.year)
            else:
                anniversary.replace(year=TODAY.year-1)
        perbfml_obj = perbfml.objects.filter(perbfml_pidm=self.employee_id)
        if perbfml_obj:
            perbfml_id = perbfml_obj[0].perbfml_id
            perfmla_id_list = perfmla.objects.filter(perfmla_id=perbfml_id).filter(perfmla_begin_date__gte=anniversary).values_list('perfmla_perbfml_id')
            for p in perfmla_id_list:
                claim_unit = perefml.objects.filter(perefml_perbfmla_id=p[0]).values_list('perefml_claim_units')
                for c in claim_unit:
                    hrs_claimed += c[0]
        self.protected_leave_hrs_taken = hrs_claimed

    def query_current_paid_leaves_balances(self):
        perleav_balances = perleav.objects.filter(perleav_pidm=self.employee_id).annotate(current_leave_total=F('perleav_begin_balance') - F('perleav_taken')).values_list('perleav_leave_code', 'current_leave_total')
        # accrued paid leave Leave_balances
        phraccr_leav_codes = phraccr.objects.filter(phraccr_pidm=self.employee_id).values_list('phraccr_leav_code', flat=True).distinct()
        phraccr_balances = []
        for p in phraccr_leav_codes:
            result = phraccr.objects.filter(phraccr_pidm=self.employee_id).filter(phraccr_leav_code=p).latest('phraccr_activity_date')
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
            result = dictfetchall(cursor)
            self.paid_leave_balances = {}
            for r in result:
                self.paid_leave_balances[r["leave_code"]] = r["balance"]

    def query_reports(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM database_leavereports;")
            reports = dictfetchall(cursor)
            if reports:
                self.reports = reports

    def query_current_graph(self):
        active_graph = query_active_graph()
        if active_graph:
            self.graph = model_to_dict(active_graph)

    def query_other_employee_info(self):
        self.query_lookback_hrs()
        self.query_emails()
        self.query_fte_and_classification()
        self.query_leave_eligibility()
        self.query_deductions_info()
        self.query_protected_leave_hrs_taken()
        self.query_current_paid_leaves_balances()
        self.query_reports()
        self.query_current_graph()
        return

    def set_username(self, username: str):
        self.odin_username = username

    def set_ofla_eligibility(self, eligibility: str):
        self.ofla_eligibility = eligibility

    def set_fmla_eligibility(self, eligibility: str):
        self.fmla_eligibility = eligibility

    def get_employee_id(self):
        return self.employee_id

    def get_hire_date(self):
        return self.hire_date

    def get_fte(self):
        return self.fte
