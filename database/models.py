from django.db import models
from datetime import date
from django.db.models import Q, F, Sum
from django.db import connection

TODAY = date.today()

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
    id = models.CharField(max_length=3, primary_key=True)
    ptrearn_fmla_eligible_hrs_ind = models.CharField(max_length=1)

class pdrdedn(models.Model):
    pdrdedn_pidm =models.IntegerField()
    pdrdedn_bdca_code = models.CharField(max_length=3)
    pdrdedn_effective_date = models.DateField()
    pdrdedn_status = models.CharField(max_length = 1)
    def _str_(self):
        return self.name

'''
class leavereports(models.Model):
    leavereports_pidm = models.IntegerField(primary_key=True)
    leavereports_date = models.DateField()
    leavereports_report = models.FileField()
'''

# Helper models below

class Employee(models.Model):
    employee_id  = models.IntegerField(primary_key=True)
    odin_username = models.CharField(max_length=200)
    psu_id = models.IntegerField(default=0)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    hire_date = models.DateField()
    fte = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    month_lookback_12 = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    month_lookback_6 = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    fmla_eligibility = models.CharField(max_length=1)
    ofla_eligibility = models.CharField(max_length=1)
    deductions_eligibility = models.CharField(max_length=200)
    paid_leave_balances = models.TextField()
    protected_leave_hrs_taken = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    max_protected_leave_hrs = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

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

    # TODO: error handling for len is less than 12 and 6 months
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

    def query_fte(self):
        nbrjobs_user = nbrjobs.objects.filter(nbrjobs_pidm=self.employee_id)
        nbrbjob_user = nbrbjob.objects.filter(nbrbjob_pidm=self.employee_id).filter(nbrbjob_end_date__isnull=True)
        if (nbrbjob_user):
            for n in nbrbjob_user:
                positions = nbrjobs_user.filter(nbrjobs_posn=n.nbrbjob_posn).filter(nbrjobs_suff=n.nbrbjob_suff).exclude(Q(nbrjobs_ecls_code='XA') | Q(nbrjobs_ecls_code='XB') | Q(nbrjobs_ecls_code='XC')).values_list('nbrjobs_appt_pct').distinct()
                if (positions):
                    self.fte = max(max(positions))/100

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
            perfmla_id_list = perfmla.objects.filter(perfmla_perbfml_id=perbfml_id).filter(perfmla_begin_date__gte=anniversary).values_list('perfmla_id')
            for p in perfmla_id_list:
                print("hi")
                hrs_claimed += perefml.objects.filter(p=perefml_id).values_list('perefml_claim_units')
        self.protected_leave_hrs_taken = hrs_claimed

    def query_current_paid_leaves_balances(self):
        perleav_balances = perleav.objects.filter(perleav_pidm=self.employee_id).annotate(current_leave_total=F('perleav_begin_balance') + F('perleav_accrued') - F('perleav_taken')).values_list('perleav_leave_code', 'current_leave_total')
        with connection.cursor() as cursor:
            cursor.execute("CREATE TEMPORARY TABLE paid_leave_table (leave_code varchar(4) NOT NULL, balance decimal NULL);")
            for p in perleav_balances:
                cursor.execute("INSERT into paid_leave_table (leave_code, balance) values (%s, %s);", [p[0], p[1]])
            cursor.execute("SELECT * FROM paid_leave_table;")
            self.paid_leave_balances = cursor.fetchall()

    def query_other_employee_info(self):
        self.query_lookback_hrs()
        self.query_emails()
        self.query_fte()
        self.query_leave_eligibility()
        self.query_deductions_info()
        self.query_protected_leave_hrs_taken()
        self.query_current_paid_leaves_balances()

    def set_username(self, username: str):
        self.odin_username = username

    def get_employee_id(self):
        return self.employee_id

    def get_hire_date(self):
        return self.hire_date
