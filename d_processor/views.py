from django.shortcuts import render
from data_processor import imports as imp
from data_processor import logic as log
import inspect
from prediction.ml.registry import MLRegistry
from prediction.ml.income_classifier.random_forest import RandomForestClassifier
from prediction.ml.income_classifier.extra_trees import ExtraTreesClassifier # import ExtraTrees ML algorithm
from prediction.ml.application_classifier.random_forest import RandomForestApplicationClassifier
from prediction.ml.application_classifier.random_f import LoanApplicationClassifier 
from prediction.ml.behavioral_scoring.random_f import BehavioralScoring 
from prediction.ml.retent_scroring.random_f import  RetentionScoring
from prediction.ml.application_classifier.scoring_model import LoanApplicationScoring

from rest_framework import views, status 
from rest_framework.response import Response
import os
from companies.models import Loan_History, IncomeData, LoanApplication
from data_processor.get_pred import GetPredictions as gpred
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.

def importer(request):
    path_to_artifacts = os.path.join(BASE_DIR, 'prediction/ml/algo_data/files/')
    opfile =  path_to_artifacts + 'no_header_data.csv'
    # lon_hist_file =  path_to_artifacts + 'companies_loan_history.csv'
    imp.get_data_income_data(opfile)
    # imp.get_data(lon_hist_file)
    data = LoanApplication.objects.all()
    context = {
        'data':data,
    }
    return render(request,'test.html', context)

def test(request):
    data = Loan_History.objects.all()
    return_data = log.grade_avg(data)
    context = {
        'webdata':return_data
    }
    return render(request, 'test.html', context)


def dash(request):

    return render("dash.html")

def dashboard(request):
    data = Loan_History.objects.all()
    return_data = log.grade_avg(data)
    context = {
        'webdata':return_data
    }
    return render(request, "dashboard-chartsjs.html", context)


def add_algo(request):
    # ML registry
    try:
        print("Adding ML algorithms to registry")
        registry = MLRegistry() # create ML registry
        # Random Forest classifier
        rf = RandomForestClassifier()
        # add to ML registry
        registry.add_algorithm(endpoint_name="income_classifier",
                                algorithm_object=rf,
                                algorithm_name="random forest",
                                algorithm_status="production",
                                algorithm_version="0.0.1",
                                owner="Dreatol",
                                algorithm_description="Random Forest with simple pre- and post-processing",
                                algorithm_code=inspect.getsource(RandomForestClassifier))

        # Applications Random Forest classifier
        # aprf = RandomForestApplicationClassifier()
        # # add to ML registry
        # registry.add_algorithm(endpoint_name="application_classifier",
        #                         algorithm_object=aprf,
        #                         algorithm_name="random forest",
        #                         algorithm_status="production",
        #                         algorithm_version="0.0.1",
        #                         owner="Dreatol",
        #                         algorithm_description="Random Forest with simple pre- and post-processing",
        #                         algorithm_code=inspect.getsource(RandomForestApplicationClassifier))

        ln_rf = LoanApplicationClassifier()
        # add to ML registry
        registry.add_algorithm(endpoint_name="loan_application_classifier",
                                algorithm_object=ln_rf,
                                algorithm_name="random forest",
                                algorithm_status="production",
                                algorithm_version="0.0.1",
                                owner="Dreatol",
                                algorithm_description="55 features Random Forest with simple pre- and post-processing",
                                algorithm_code=inspect.getsource(LoanApplicationClassifier))

        behavioral_scoring = BehavioralScoring()
        # add to ML registry
        registry.add_algorithm(endpoint_name="behavioral_scoring",
                                algorithm_object=behavioral_scoring,
                                algorithm_name="random forest",
                                algorithm_status="production",
                                algorithm_version="0.0.1",
                                owner="Dreatol",
                                algorithm_description="55 features Random Forest with simple pre- and post-processing",
                                algorithm_code=inspect.getsource(BehavioralScoring))

        retention_scoring = RetentionScoring()
        # add to ML registry
        registry.add_algorithm(endpoint_name="retention_scoring",
                                algorithm_object=retention_scoring,
                                algorithm_name="random forest",
                                algorithm_status="production",
                                algorithm_version="0.0.1",
                                owner="Dreatol",
                                algorithm_description="55 features Random Forest with simple pre- and post-processing",
                                algorithm_code=inspect.getsource(RetentionScoring))



        # LoanApplicationScoring
        ls = LoanApplicationScoring()
        # add to ML registry

        registry.add_algorithm(endpoint_name="loan_application_scoring",
                                algorithm_object=ls,
                                algorithm_name="random forest",
                                algorithm_status="production",
                                algorithm_version="0.0.1",
                                owner="Dreatol",
                                algorithm_description="LoanApplicationScoring with simple pre- and post-processing",
                                algorithm_code=inspect.getsource(LoanApplicationScoring))
        print("Added ML algorithms to registry")
    except Exception as e:
        print("Exception while loading the algorithms to the registry,", str(e))
        error = str(e)

    context = {
        'registry':registry,
    }
    return render(request, "test.html", context)


def run_predictions(request):
    qry = Loan_History.objects.all()[:5]
    retention_scoring_data = gpred.get_retention_scores(qry)
    application_classifier_data = gpred.get_application_scores(qry)
    behavioral_classifier_data = gpred.get_behavioral_scores(qry)
    context = {
        'message':'successful ran predictions',
    }   
    return render(request, "test.html", context)