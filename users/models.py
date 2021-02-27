from django.db import models
from decimal import Decimal as D
from .UserManager import UserManager
from django.contrib.auth.hashers import get_hasher, identify_hasher
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
class Role(models.Model):
    owner = 'owner'
    officer = 'officer'
    manager = 'manager'
    admin = 'admin'
    executive = 'executive'
    client = 'client'
    field_officer = 'field_officer'
    internal_officer = 'internal_officer'
    USER_GROUP_CHOICES = [
            (client,'client'),
            (executive,'executive'),
            (field_officer,'field_officer'),
            (internal_officer,'internal_officer'),
        ]

    ROLE_CHOICES = [
            (client,'client'),
            (owner,'owner'),
            (officer,'officer'),
            (manager,'manager'),
            (admin,'admin'),
        ]
    name = models.CharField(max_length=70, choices=ROLE_CHOICES, default = officer)
    user_group = models.CharField(max_length=70, choices=USER_GROUP_CHOICES, default = field_officer)

    def __str__(self):
        return self.name



class AccountUser(models.Model):
    user_role = models.ForeignKey(Role, on_delete = models.CASCADE , null=True, blank=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE , null=True, blank=True)
    # first_name = models.CharField(max_length=100, null=True, blank=True)
    # last_name = models.CharField(max_length=100, null=True, blank=True)  
    # email = models.EmailField(unique=True,db_index=True, null=True, blank=True)  
    category = models.CharField(null=True ,blank=True,max_length=70)
    work_email = models.CharField(null=True ,blank=True,max_length=70)
    personal_email = models.CharField(null=True ,blank=True,max_length=70)
    age = models.IntegerField(null=True ,blank=True)
    email_confirmed = models.BooleanField(default=False)
    accepted_terms = models.BooleanField(default=False)
    home_address = models.TextField(null=True ,blank=True)
    date_birth =models.DateField(null=True ,blank=True)
    phone =models.CharField(null=True ,blank=True,max_length=70)
    id_number =models.CharField(null=True ,blank=True,max_length=20)
    gender =models.CharField(null=True ,blank=True,max_length=20)
    education_level =models.CharField(null=True ,blank=True,max_length=70)
    marital_status =models.CharField(null=True ,blank=True,max_length=20)
    number_dependants =models.IntegerField(null=True ,blank=True)
    profile_pic = models.ImageField(null=True ,blank=True, upload_to='staticfiles/images')
    facebookId = models.CharField(max_length=100, null=True, blank=True,db_index=True)
    android = models.BooleanField(blank=True, default=False)
    ios = models.NullBooleanField(blank=True, default=False, null=True)
    acceptPush = models.BooleanField(default=False)
    pushToken = models.CharField(max_length=100, null=True, blank=True,db_index=True)
    is_active = models.BooleanField(('active'), default=True)
    is_staff = models.BooleanField(('staff'), default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    class Meta:
        verbose_name = ('User')
        verbose_name_plural = ('Users')



class Organization(models.Model):
    orga_id = models.CharField(max_length=100, null=True, blank=True,db_index=True)
    owner = models.ForeignKey(AccountUser, related_name="organization", verbose_name="Micro Finance Director", on_delete = models.CASCADE)
    business_name = models.CharField(max_length=70,null=True ,blank=True)
    business_trading_name = models.CharField(max_length=70,null=True ,blank=True)
    registration_number = models.CharField(max_length=70,null=True ,blank=True)
    bp_number = models.CharField(max_length=70,null=True ,blank=True)
    entity_type = models.CharField(max_length=70,null=True ,blank=True)
    business_category = models.CharField(max_length=70,null=True ,blank=True)
    registered_byuser_as = models.ForeignKey(Role, verbose_name="Admin", on_delete = models.CASCADE,null=True ,blank=True)
    total_branches =models.IntegerField(null=True ,blank=True)
    profile_pic = models.ImageField(null=True ,blank=True, upload_to='staticfiles/images')
    address =models.TextField(null=True ,blank=True)
    phone =models.CharField(null=True ,blank=True,max_length=70)
    logo = models.ImageField(upload_to="media/%Y/%m/%d",null=True, blank=True)
    icon = models.ImageField(upload_to="media/%Y/%m/%d",null=True, blank=True)
    image1 = models.ImageField(upload_to="media/%Y/%m/%d",null=True, blank=True)
    statement =models.TextField(null=True ,blank=True)
    acceptPush = models.BooleanField(default=False)
    pushToken = models.CharField(max_length=100, null=True, blank=True,db_index=True)
    is_active = models.BooleanField(('active'), default=True)
    is_verified = models.BooleanField(('active'), default=False)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ('Organization')
        verbose_name_plural = ('Organizations')



class Manager(models.Model):
    manager_id = models.CharField(max_length=100, null=True, blank=True,db_index=True)
    profile = models.ForeignKey(AccountUser, related_name="manager", verbose_name="Manager Account", on_delete = models.CASCADE,null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete = models.CASCADE,null=True, blank=True)
    # department =  models.ForeignKey(Department, on_delete=models.CASCADE,null=True ,blank=True)
    signup_date = models.DateTimeField(auto_now=True)


class Department(models.Model):
    organization =  models.ForeignKey(Organization, related_name="department", verbose_name="Department", on_delete=models.CASCADE, default=0)
    name = models.CharField(null=True ,blank=True,max_length=20)
    manager = models.ForeignKey(Manager, related_name="department", on_delete = models.CASCADE,null=True, blank=True)
    mission =models.TextField(null=True ,blank=True)
    vision =models.TextField(null=True ,blank=True)
    statement =models.TextField(null=True ,blank=True)
    image = models.ImageField(upload_to="media/%Y/%m/%d",null=True, blank=True)
    video = models.FileField(upload_to="media/%Y/%m/%d",null=True, blank=True)
    def __str__(self):
        return self.name

class LoanOfficer(models.Model):
    officer_id = models.CharField(max_length=100, null=True, blank=True,db_index=True)
    manager = models.ForeignKey(Manager, verbose_name="Manager", on_delete = models.CASCADE,null=True, blank=True)
    profile = models.ForeignKey(AccountUser, related_name="officer", verbose_name="Officer Account", on_delete = models.CASCADE,null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete = models.CASCADE,null=True, blank=True)
    department =  models.ForeignKey(Department, on_delete=models.CASCADE,null=True ,blank=True)
    signup_date = models.DateTimeField()



class Clients(models.Model):
    client_id = models.CharField(max_length=100, null=True, blank=True,db_index=True)
    profile = models.ForeignKey(AccountUser, related_name="client", verbose_name="Client", on_delete = models.CASCADE,null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete = models.CASCADE,null=True, blank=True)
    signing_officer = models.ForeignKey(LoanOfficer, related_name="client_account_officer", verbose_name="Account Officer", on_delete = models.CASCADE,null=True, blank=True)
    department =  models.ForeignKey(Department, on_delete=models.CASCADE,null=True ,blank=True)
    registration_date = models.DateTimeField()


class Loan(models.Model):
    school_fees = 'school_fees'
    business = 'business'
    mortage = 'mortage'
    funeral_assistance = 'funeral_assistance'
    
    LOAN_TYPE = [
            (business,'business'),
            (school_fees,'school_fees'),
            (mortage,'mortage'),
            (funeral_assistance,'funeral_assistance'),
        ]
    loan_id = models.CharField(max_length=100, null=True, blank=True,db_index=True)
    loan_type = models.CharField(max_length=70, choices=LOAN_TYPE, default = school_fees)
    signing_officer = models.ForeignKey(LoanOfficer, related_name="loan_officer", verbose_name="Account Officer", on_delete = models.CASCADE,null=True, blank=True)
    client = models.ForeignKey(Clients, related_name="loan_client", verbose_name="Client", on_delete = models.CASCADE,null=True, blank=True)
    application_date = models.DateTimeField(null=True ,blank=True)
    approval_date = models.DateTimeField(null=True ,blank=True)
    loan_term =models.CharField(null=True ,blank=True,max_length=20)
    colleteral = models.CharField(null=True ,blank=True,max_length=20)
    amount= models.CharField(null=True ,blank=True,max_length=20)
