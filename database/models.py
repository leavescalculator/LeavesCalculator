from django.db import models

class gobeacc(models.Model):
    gobeacc_pidm = models.IntegerField(primary_key=True)
    gobeacc_username = models.CharField(max_length=30)

class goremal(models.Model):
    goremal_pidm = models.IntegerField(primary_key=True)
    goremal_emal_code = models.CharField(max_length=4)
    goremal_email_address = models.CharField(max_length=128)

class gorsdav(models.Model):
    gorsdav_table_name = models.CharField(max_length=30)
    gorsdav_attr_name = models.CharField(max_length=30)
    gorsdav_pk_parenttab = models.CharField(max_length=512)   
    gorsdav_value = models.CharField(max_length=1)

class nbrjobs(models.Model):
    nbrjobs_pidm = models.IntegerField(primary_key=True)
    nbrjobs_posn = models.CharField(max_length=6)
    nbrjobs_suff = models.CharField(max_length=2)
    nbrjobs_effective_date = models.DateTimeField('date_started')
    nbrjobs_ecls_code = models.CharField(max_length=2)
    nbrjobs_appt_pct = models.IntegerField()

class nbrjob(models.Model):
    nbrjob_pidm = models.IntegerField(primary_key=True)
    nbrjob_posn = models.CharField(max_length=6)
    nbrjob_suff = models.CharField(max_length=2)
    nbrjob_contract_type = models.CharField(max_length=1)

class spriden(models.Model):
    spriden_pidm = models.IntegerField(primary_key=True)
    spriden_id = models.CharField(max_length=9)
    spriden_last_name = models.CharField(max_length=60)
    spriden_first_name = models.CharField(max_length=60)

class pebempl(models.Model):
    pebempl_pidm = models.IntegerField(primary_key=True)
    pebempl_empl_status = models.CharField(max_length=1)
    pebempl_first_hire_date = models.DateTimeField('date_started')

class phraccr(models.Model):
    phraccr_pidm =  models.IntegerField(primary_key=True)
    phraccr_leav_code = models.CharField(max_length=4)
    phraccr_curr_accr = models.IntegerField()
    phraccr_activity_date = models.DateTimeField('activity date')

class perleav(models.Model):
    perleav_pidm = models.IntegerField(primary_key=True)
    perleav_leave_code = models.CharField(max_length=4)
    perleav_begin_balance = models.IntegerField()
    perleav_accrued = models.IntegerField()
    perleav_taken = models.IntegerField()
    Current_Balance = models.IntegerField()

class perefml(models.Model):
    perefml_id = models.IntegerField(primary_key=True)
    perefml_perbfmla_id = models.IntegerField()
    perefml_earn_code = models.CharField(max_length=3)
    perefml_claim_units = models.IntegerField()

class perfmla(models.Model):
    perfmla_id = models.IntegerField(primary_key=True)
    perfmla_perbfml_id = models.IntegerField()
    perfmla_begin_date = models.DateTimeField('begin date');

class perbfml(models.Model):
    perbfml_id = models.IntegerField(primary_key=True)
    perbfml_pidm = models.IntegerField()
    perbfml_max_units = models.IntegerField()

class perjtot(models.Model):
    perjtot_pidm = models.IntegerField(primary_key=True)
    perjtot_earn_code = models.CharField(max_length=3)
    perjtot_year = models.IntegerField()
    perjtot_month = models.IntegerField()
    perjtot_hrs = models.IntegerField()

class ptearn(models.Model):
    ptearn_code = models.CharField(max_length=3, primary_key=True)
    ptearn_fmla_eligible_hrs_ind = models.CharField(max_length=1)

class pdrdedn(models.Model): 
    pdrdedn_pidm = models.IntegerField(primary_key=True)
    pdrdedn_bdca_code = models.CharField(max_length=3)
    pdrdedn_effective_date = models.DateTimeField('effective date')
    pdrdedn_status = models.CharField(max_length = 1)





