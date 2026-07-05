from django.db import models
from django.utils.timezone import now

from masters.models import Branch, Vendor


# Create your models here.


class Transaction(models.Model):
    voucher_no = models.CharField(max_length=20,null=True,blank=True)
    transaction_date = models.DateField(null=True,blank=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    gl_no =  models.CharField(max_length=48,null=True,blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.00,max_digits=18,decimal_places=2)
    dr_cr_in = models.IntegerField(null=True,blank=True)
    remarks = models.CharField(max_length=48,null=True,blank=True)
    created_date = models.DateTimeField(default=now)


class validation_log(models.Model):
    upload_batch_no = models.CharField(max_length=20,null=True,blank=True)
    row_no = models.IntegerField(null=True,blank=True)
    voucher_no = models.CharField(max_length=20,null=True,blank=True)
    vendor_code =  models.CharField(max_length=20,null=True,blank=True)
    gl_code =  models.CharField(max_length=20,null=True,blank=True)
    branch_code =  models.CharField(max_length=20,null=True,blank=True)
    amount = models.DecimalField(default=0.00,max_digits=18,decimal_places=2)
    error_type = models.CharField(max_length=500,null=True,blank=True)
    error_message = models.CharField(max_length=500,null=True,blank=True)
    status = models.IntegerField(null=True,blank=True)
    created_date = models.DateTimeField(default=now)
    created_by = models.IntegerField(null=True,blank=True)