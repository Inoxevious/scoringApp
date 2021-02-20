from django.shortcuts import render
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVector, TrigramSimilarity,
)
from mergedeep import merge
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q, F
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
import csv
from io import StringIO
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.http import HttpResponse, StreamingHttpResponse
from django.utils.text import slugify
import json # will be needed for saving preprocessing details
import numpy as np # for data manipulation
import pandas as pd # for data manipulation
from sklearn.model_selection import train_test_split # will be used for data split
import requests
from prediction.ml.income_classifier import random_forest as rf
from prediction.ml.income_classifier import  extra_trees as et

from prediction.models import Endpoint
from prediction.serializers import EndpointSerializer

from prediction.models import MLAlgorithm
from prediction.serializers import MLAlgorithmSerializer

from prediction.models import MLAlgorithmStatus
from prediction.serializers import MLAlgorithmStatusSerializer

from prediction.models import MLRequest
from prediction.serializers import MLRequestSerializer
import json
from numpy.random import rand
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.views import APIView
from prediction.ml.registry import MLRegistry
# from fintechapp.wsgi import registry
from django.db import transaction
from users.models import Clients, LoanOfficer, Loan, AccountUser, Organization
from companies.models import *
from django.forms.models import model_to_dict
# Create your views here.
from data_processor import imports as imp
from data_processor import logic as log
from datetime import datetime, date
from django.db.models import Sum
from prediction.ml.income_classifier.random_forest import RandomForestClassifier
from prediction.ml.income_classifier.extra_trees import ExtraTreesClassifier
from prediction.ml.application_classifier.random_forest import RandomForestApplicationClassifier

from django.http import JsonResponse

from rest_framework.views import APIView
from .serializers import *
from .models import Loan_History, IncomeData
from .pagination import StandardResultsSetPagination
from .get_income_pred import GetPredictions as gpred
from prediction.models import BehaviouralScores
from prediction.models import  RetentionScores
from prediction.models import  ApplicationScores

class Index(TemplateView):
    template_name = "finapp/index.html"

class ApplicationAPIView(APIView):

    def get(self, request):
        # pagination_class = StandardResultsSetPagination
        # serializer_class = ApplicationScoresSerializer(many=True)
        # filter the queryset based on the filters applied
        global qry
        queryList = ApplicationScores.objects.all()
        loan_officer = self.request.query_params.get('loan_officer', None)
        # ORGANIZATION_TYPE = self.request.query_params.get('mortage', None)
        # OCCUPATION_TYPE = self.request.query_params.get('funeral', None)
        # CODE_GENDER = self.request.query_params.get('school', None)
        sort_by = self.request.query_params.get('sort_by', None)

        if loan_officer:
            queryList = ApplicationScores.objects.filter(loan_officer = loan_officer)[:5]
  
        # sort it if applied on based on price/points
        if sort_by == "income":
            queryList = queryList.order_by("client_id")
        elif sort_by == "credit_amount":
            queryList = queryList.order_by("loan_amount")
# get predictions for applications scoring predictions
        # application_classifier_data = gpred.get_application_scores(queryList)
        data = ApplicationScoresSerializer(queryList, many=True).data
        return  Response(data)

class BehavioralAPIView(APIView):
    def get(self, request):
        pagination_class = StandardResultsSetPagination
        serializer_class = BehaviouralScoresSerializer
        # filter the queryset based on the filters applied
        global qry
        queryList = BehaviouralScores.objects.all()
        loan_officer = self.request.query_params.get('loan_officer', None)
        # ORGANIZATION_TYPE = self.request.query_params.get('mortage', None)
        # OCCUPATION_TYPE = self.request.query_params.get('funeral', None)
        # CODE_GENDER = self.request.query_params.get('school', None)
        sort_by = self.request.query_params.get('sort_by', None)

        if loan_officer:
            queryList = BehaviouralScores.objects.filter(loan_officer = loan_officer)[:5]
  
        # sort it if applied on based on price/points
        if sort_by == "income":
            queryList = queryList.order_by("client_id")
        elif sort_by == "credit_amount":
            queryList = queryList.order_by("loan_amount")
        data = BehaviouralScoresSerializer(queryList, many=True).data
        data = {"behavioural_data":data}
        return Response(data) 






class RetentionAPIView(APIView):
    def get(self, request):
        pagination_class = StandardResultsSetPagination
        serializer_class = RetentionScoresSerializer
        # filter the queryset based on the filters applied
        global qry
        queryList = RetentionScores.objects.all()
        loan_officer = self.request.query_params.get('loan_officer', None)
        # ORGANIZATION_TYPE = self.request.query_params.get('mortage', None)
        # OCCUPATION_TYPE = self.request.query_params.get('funeral', None)
        # CODE_GENDER = self.request.query_params.get('school', None)
        sort_by = self.request.query_params.get('sort_by', None)

        if loan_officer:
            queryList = RetentionScores.objects.filter(loan_officer = loan_officer)[:5]
  
        # sort it if applied on based on price/points
        if sort_by == "income":
            queryList = queryList.order_by("client_id")
        elif sort_by == "credit_amount":
            queryList = queryList.order_by("loan_amount")
# get predictions for applications scoring predictions
        # application_classifier_data = gpred.get_application_scores(queryList)
        data = RetentionScoresSerializer(queryList, many=True).data
        data = {"retention_data":data}
        return  Response(data)

class HomeView(ListView):
    template_name = 'dashboards/landing/index.html'
    def get_queryset(self, **kwargs):
        global cust_data, loan, user_name, input_data,acc_user, time
        user_id = self.request.session['account_user_id']
        time = end = datetime.today()
        acc_user = AccountUser.objects.get(id=user_id)
        user_name = acc_user
        org = Organization.objects.get(id=1)
        client = Clients.objects.filter(insti=org)

    def get_context_data(self, **kwargs):
        context = {
            'user_name':user_name,
            'acc_user':acc_user,
        }
        return context

class ProfileView(ListView):
    template_name = 'dashboards/clients/profile/index.html'
    def get_queryset(self, **kwargs):
        global cust_data, loan, user_name, input_data,acc_user, time, client
        user_id = self.request.session['account_user_id']
        id = self.request.GET.get('client_id', None)
        print(id)
        time = end = datetime.today()
        acc_user = AccountUser.objects.get(id=user_id)
        client = Clients.objects.all()[:1]
        user_name = acc_user
        print("acc_user",acc_user)
        org = Organization.objects.get(id=1)
        client = Clients.objects.filter(insti=org)

    def get_context_data(self, **kwargs):
        context = {
            'user_name':user_name,
            'acc_user':acc_user,
            'client':client,
        }
        return context

class ApplicationReportExportCsvView(ListView):
    template_name = 'dashboards/clients/profile/index.html'
    def get_queryset(self, **kwargs):
        global cust_data, loan, user_name, input_data,acc_user, time
        user_id = self.request.session['account_user_id']
        time = end = datetime.today()
        acc_user = AccountUser.objects.get(id=user_id)
        user_name = acc_user
        print("acc_user",acc_user)
        org = Organization.objects.get(id=1)
        client = Clients.objects.filter(insti=org)

    def get_context_data(self, **kwargs):
        context = {
            'user_name':user_name,
            'acc_user':acc_user,
        }
        return context

class ApplicationReportView(ListView):
    template_name = 'dashboards/clients/profile/index.html'
    def get_queryset(self, **kwargs):
        global cust_data, loan, user_name, input_data,acc_user, time
        user_id = self.request.session['account_user_id']
        time = end = datetime.today()
        acc_user = AccountUser.objects.get(id=user_id)
        user_name = acc_user
        print("acc_user",acc_user)
        org = Organization.objects.get(id=1)
        client = Clients.objects.filter(insti=org)

    def get_context_data(self, **kwargs):
        context = {
            'user_name':user_name,
            'acc_user':acc_user,
        }
        return context

class BehavioralAnalyticsResultsView(ListView):
    template_name = 'dashboards/behavioral/index.html'
    def get_queryset(self, **kwargs):
        global cust_data, loan, user_name, input_data,acc_user, time
        user_id = self.request.session['account_user_id']
        time = end = datetime.today()
        acc_user = AccountUser.objects.get(id=user_id)
        user_name = acc_user
        org = Organization.objects.get(id=1)
        client = Clients.objects.filter(insti=org)
        
    def get_context_data(self, **kwargs):
        context = {
            'user_name':user_name,
            'acc_user':acc_user,
        }
        return context


class ApplicationAnalyticsResultsView(ListView):
    template_name = 'dashboards/application/index.html'
    def get_queryset(self, **kwargs):
        global cust_data, loan, user_name, input_data,acc_user, time
        user_id = self.request.session['account_user_id']
        time = end = datetime.today()
        acc_user = AccountUser.objects.get(id=user_id)
        user_name = acc_user
        org = Organization.objects.get(id=1)
        client = Clients.objects.filter(insti=org)

    def get_context_data(self, **kwargs):
        context = {
            'user_name':user_name,
            'acc_user':acc_user,
        }
        return context

class RetentionAnalyticsResultsView(ListView):
    template_name = 'dashboards/retention/index.html'
    def get_queryset(self, **kwargs):
        global cust_data, loan, user_name, input_data,acc_user, time
        user_id = self.request.session['account_user_id']
        time = end = datetime.today()
        acc_user = AccountUser.objects.get(id=user_id)
        user_name = acc_user
        org = Organization.objects.get(id=1)
        client = Clients.objects.filter(insti=org)

    def get_context_data(self, **kwargs):
        context = {
            'user_name':user_name,
            'acc_user':acc_user,
        }
        return context


def client_profile(request):
    id = request.GET.get('client_id', None)
    print(id)
    
    
    if  Clients.objects.filter(id=id).exists():
        client = Clients.objects.get(id=id)
        print(client)
    else:
        redirect('companies:index')

    print("client", client)
    context = {
        'client':client,
    }
    return render(request,'dashboards/clients/profile/index.html', context)

def officer_profile(request):
    id = request.GET.get('officer_id', None)
    print(id)
    officer = LoanOfficer.objects.get(id=id)
    print("officer", officer)
    context = {
        'officer':officer,
    }
    return render(request,'dashboards/officers/profile/index.html', context)


def application_report_export_csv(request):
    id = request.GET.get('loan_id', None)
    print(id)
    officer = Loan.objects.get(loan_id=id)
    print("loan", loan)
    return render(request,'dashboards/articles/index.html')

def application_report(request):
    id = request.GET.get('loan_id', None)
    print(id)
    officer = Loan.objects.get(loan_id=id)
    print("loan", loan)
    return render(request,'dashboards/articles/index.html')

def reports(request):
    return render(request,'dashboards/reports/index.html')

def articles(request):
    return render(request,'dashboards/articles/index.html')

import csv
from django.http import HttpResponse
def some_view(request):
# Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    return response




#Get Business Loan Filter
def getBusiness(request):
    # get all the business loans from the database excluding 
    # null and blank values

    if request.method == "GET" and request.is_ajax():

        # business = LoanOfficer.objects.exclude(id__isnull=True).\
        #     exclude(insti__exact='').order_by('insti').values_list('insti').distinct()
        # business = [i[0] for i in list(business)]
        insti = Organization.objects.all()[:1]
        loan_officer = LoanOfficer.objects.filter(insti=insti).order_by('info__user__username').values_list('info__user__username').distinct()
        loan_officer = [i[0] for i in list(loan_officer)]
        print("loan_officer",loan_officer)
        data = {
            "loan_officer": loan_officer, 
        }
        return JsonResponse(data, status = 200)

#Get mortage Loan Filter
def getMortage(request):
    # get all the mortage loans from the database excluding 
    # null and blank values

    if request.method == "GET" and request.is_ajax():
        mortage = ApplicationScores.objects.exclude(income_text__isnull=True).\
            exclude(income_text__exact='').order_by('income_text').values_list('income_text').distinct()
        mortage = [i[0] for i in list(mortage)]
        data = {
            "mortage": mortage, 
        }
        return JsonResponse(data, status = 200)

#Get funeral Loan Filter
def getFuneral(request):
    # get all the funeral loans from the database excluding 
    # null and blank values

    if request.method == "GET" and request.is_ajax():
        funeral = ApplicationScores.objects.exclude(income_text__isnull=True).\
            exclude(income_text__exact='').order_by('income_text').values_list('income_text').distinct()
        funeral = [i[0] for i in list(funeral)]
        data = {
            "funeral": funeral, 
        }
        return JsonResponse(data, status = 200)


#Get mortage Loan Filter
def getSchool(request):
    # get all the school loans from the database excluding 
    # null and blank values

    if request.method == "GET" and request.is_ajax():
        school = ApplicationScores.objects.exclude(income_text__isnull=True).\
            exclude(income_text__exact='').order_by('income_text').values_list('income_text').distinct()
        school = [i[0] for i in list(school)]
        data = {
            "school": school, 
        }
        return JsonResponse(data, status = 200)

def data_for_charts(request):
    labels = []
    data ={}
    chart_data = {}
    queryset =  Loan_History.objects.values('OCCUPATION_TYPE').annotate(amount_borrowed=Sum('AMT_CREDIT')).order_by('-amount_borrowed')
    for entry in queryset:
        data[entry['OCCUPATION_TYPE']] = []
        # chart_data['label'] = entry['OCCUPATION_TYPE']
        data[entry['OCCUPATION_TYPE']].append(entry['amount_borrowed'])
    # data = merge(data,chart_data)
    return JsonResponse(data={
        # 'labels': labels,
        'data': data,
    })


def data_aggretation(request):
    labels = []
    data = []
    queryset =  Loan_History.objects.values('OCCUPATION_TYPE').annotate(amount_borrowed=Sum('AMT_CREDIT')).order_by('-amount_borrowed')
    for entry in queryset:
        labels.append(entry['OCCUPATION_TYPE'])
        data.append(entry['amount_borrowed'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def live_app_score_pred(request):
    algorithm_object = RandomForestClassifier()
    # posts = Post.objects.all()
    response_data = {}
    context = {}
    if request.method == 'POST':
        age = request.POST.get('age') 
        workclass = request.POST.get('workclass') 
        fnlwgt = request.POST.get('fnlwgt') 
        education = request.POST.get('education') 
        education_num = request.POST.get('education_num') 
        marital_status = request.POST.get('marital_status') 
        occupation = request.POST.get('occupation') 
        relationship = request.POST.get('relationship') 
        race = request.POST.get('race') 
        sex = request.POST.get('sex') 
        capital_gain = request.POST.get('capital_gain') 
        capital_loss = request.POST.get('capital_loss') 
        hours_per_week = request.POST.get('hours_per_week') 
        native_country = request.POST.get('native_country') 

        data ={'age':  age, 'workclass':  workclass, 
        'fnlwgt':  fnlwgt, 'education':  education, 
        'education-num':  education_num, 'marital-status':  marital_status, 
        'occupation': occupation, 'relationship':  relationship, 
        'race':  race, 'sex':  sex, 'capital-gain':  capital_gain, 
        'capital-loss':  capital_loss, 'hours-per-week':  hours_per_week, 
        'native-country':  native_country
        }
        incomes_prediction = {}
        print("incomes_prediction data", data)
        incomes_prediction = algorithm_object.compute_prediction(data) 
        print("incomes_prediction data", incomes_prediction)
        if  incomes_prediction['income_probability'] > 0.67:
            color = 'red'
            text = 'high risk'
            incomes_prediction["income_color"] = color
            incomes_prediction["income_text"] = text
        elif  incomes_prediction['income_probability'] > 0.33:
            color = 'blue'
            text = 'moderate risk'
            incomes_prediction["income_color"] = color
            incomes_prediction["income_text"] = text
        else:
            color = 'green'
            text = 'low risk'
            incomes_prediction["income_color"] = color
            incomes_prediction["income_text"] = text
        data = {
            "incomes_prediction": incomes_prediction, 
        }
        context = {
            'result': "prediction successful",
            'incomes_prediction':incomes_prediction,
        }

        return render(request,'dashboards/officers/predictions/index.html', context)

    context = {
        'result': "fail",
        
    }
    return render(request,'dashboards/officers/predictions/index.html', context)