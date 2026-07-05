from django.db import models
from django.utils.timezone import now


# Create your models here.


class trial_balance(models.Model):
    financial_year = models.IntegerField(null=True,blank=True)
    financial_month = models.IntegerField(null=True,blank=True)
    branch_id = models.IntegerField(null=True,blank=True)
    gl =  models.CharField(max_length=48,null=True,blank=True)
    opening_balance = models.DecimalField(max_digits=16, decimal_places=2, null=False, blank=False)
    debit = models.DecimalField(max_digits=16, decimal_places=2, null=False, blank=False)
    credit = models.DecimalField(max_digits=16, decimal_places=2, null=False, blank=False)
    closing_balance = models.DecimalField(max_digits=16, decimal_places=2, null=False, blank=False, db_index=True)
    status = models.IntegerField(null=True,blank=True)
    created_date = models.DateTimeField(default=now)