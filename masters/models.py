from django.db import models
from django.utils.timezone import now


# Create your models here.

class Vendor(models.Model):
    vendor_code = models.CharField(max_length=32,null=True,blank=True)
    vendor_name = models.CharField(max_length=32,null=True,blank=True)
    status = models.IntegerField(default=1)
    created_date = models.DateTimeField(default=now)

class GL(models.Model):
    gl_no = models.CharField(max_length=30,null=True,blank=True)
    gl_type = models.CharField(max_length=30,null=True,blank=True)
    gl_desc = models.CharField(max_length=100,null=True,blank=True)
    status = models.IntegerField(default=1)
    created_date = models.DateTimeField(default=now)

class Branch(models.Model):
    branch_code = models.CharField(max_length=30,null=True,blank=True)
    branch_name = models.CharField(max_length=100,null=True,blank=True)
    status = models.IntegerField(default=1)
    created_date = models.DateTimeField(default=now)