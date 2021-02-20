from django.apps import AppConfig
import pandas as pd
from joblib import load
import os

class PredictionConfig(AppConfig):
    name = 'prediction'
# LOADING MODEL FILES
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MLMODEL_FOLDER = os.path.join(BASE_DIR, 'prediction/mlmodel/')
    MLMODEL_FILE = os.path.join(MLMODEL_FOLDER, "IRISRandomForestClassifier.joblib")

    # APPLICATION SCORING 
    LoanApplicationScoringModel_FILE = os.path.join(MLMODEL_FOLDER, "score_model.pkl")

    # RETENTION SCORING
    retention_values_fill_missing = retention_values_fill_missing_FILE =  os.path.join(MLMODEL_FOLDER, "train_mode.joblib")
    retention_encoders = retention_encoders_FILE = os.path.join(MLMODEL_FOLDER, "encoders.joblib")
    retention_model_FILE = os.path.join(MLMODEL_FOLDER, "random_forest.joblib")
    # 

    # BehavioralScoring

# LOADING MODELS
    irismlmodel = load(MLMODEL_FILE)


    # APPLICATION SCORING  MODEL
    applicationscoringmodel = load(LoanApplicationScoringModel_FILE)

    # RETENTION SCORING  MODEL
    retention_values_fill_missing = load(retention_values_fill_missing_FILE)
    retention_encoders = load(retention_encoders_FILE)
    retention_model = load(retention_model_FILE)


    # Behavioral SCORING MODEL
     
