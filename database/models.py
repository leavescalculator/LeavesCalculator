from django.db import models

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
    id = models.IntegerField(primary_key=True)
    nbrjobs_posn = models.CharField(max_length=6)
    nbrjobs_suff = models.CharField(max_length=2)
    nbrjobs_effective_date = models.DateField()
    nbrjobs_ecls_code = models.CharField(max_length=2)
    nbrjobs_appt_pct = models.IntegerField()
    def _str_(self):
        return self.name

class nbrjob(models.Model):
    id = models.IntegerField(primary_key=True)
    nbrjob_posn = models.CharField(max_length=6)
    nbrjob_suff = models.CharField(max_length=2)
    nbrjob_contract_type = models.CharField(max_length=1)
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
    pebempl_first_hire_date = models.DateField(auto_now=False)
    def _str_(self):
        return self.name

class phraccr(models.Model):
    id =  models.IntegerField(primary_key=True)
    phraccr_leav_code = models.CharField(max_length=4)
    phraccr_curr_accr = models.IntegerField()
    phraccr_activity_date = models.DateField()
    def _str_(self):
        return self.name

class perleav(models.Model):
    id = models.IntegerField(primary_key=True)
    perleav_leave_code = models.CharField(max_length=4)
    perleav_begin_balance = models.IntegerField()
    perleav_accrued = models.IntegerField()
    perleav_taken = models.IntegerField()
    Current_Balance = models.IntegerField()
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
    id = models.IntegerField(primary_key=True)
    perfmla_perbfml_id = models.IntegerField()
    perfmla_begin_date = models.DateField();
    def _str_(self):
        return self.name

class perbfml(models.Model):
    id = models.IntegerField(primary_key=True)
    perbfml_pidm = models.IntegerField()
    perbfml_max_units = models.IntegerField()
    def _str_(self):
        return self.name

class perjtot(models.Model):
    id = models.IntegerField(primary_key=True)
    perjtot_earn_code = models.CharField(max_length=3)
    perjtot_year = models.IntegerField()
    perjtot_month = models.IntegerField()
    perjtot_hrs = models.IntegerField()
    def _str_(self):
        return self.name

class ptearn(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    ptearn_fmla_eligible_hrs_ind = models.CharField(max_length=1)

class pdrdedn(models.Model): 
    id = models.IntegerField(primary_key=True)
    pdrdedn_bdca_code = models.CharField(max_length=3)
    pdrdedn_effective_date = models.DateField()
    pdrdedn_status = models.CharField(max_length = 1)
    def _str_(self):
        return self.name





