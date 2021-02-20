import numpy as np
from numpy import mean, std, hstack
import pandas as pd
import os
from sklearn.utils import shuffle
from sklearn.metrics import mean_absolute_error
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import VotingClassifier

from warnings import simplefilter
import joblib
from sklearn.exceptions import ConvergenceWarning

class LoanApplicationScoring:
    def __init__(self):
        global BASE_DIR, path_to_artifacts
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_to_artifacts = os.path.join(BASE_DIR, 'algo_data/files/')
        # self.model = pickle.load(open(path_to_artifacts + 'light_model.sav', 'rb'))
        self.modelReload = joblib.load(path_to_artifacts + './score_model.pkl')

    def preprocessing(self, input_data):
        application_data = pd.DataFrame(input_data, index=[0])
        application_data = pd.DataFrame.from_dict(application_data) 
        features = df[list(df.columns)[:-1]]
        features = self.z_score(features).values
        labels = df['default'].values 
        return features

    def z_score(df):
        df_std = df.copy()
        # apply the z-score method
        for column in df_std.columns:
            df_std[column] = (df_std[column] - df_std[column].mean()) / df_std[column].std()
        return df_std

    def predict(self, input_data):
        prob = modelReload.predict_proba(X_test)[:,-1]
        p = prob[0]
        return p

    def postprocessing(self, p):
        label = "low"
        # print("Prob",p)
        if p > 0.67:
            label = "high"
            # print('Client with ID # {} has a high risk of defaulting the loan'.format(a))
        elif p > 0.33:
            label = "moderate"
            # print('Client with ID # {} has a moderate risk of defaulting the loan'.format(a))
        else:
            label = "low"
            # print('Client with ID # {} has a low risk of defaulting the loan'.format(a))
        # print("application_probability:",p, "label:", label, "status:", "OK")    
        return {"application_probability": p, "application_label": label, "application_status": "OK"}

    def compute_prediction(self, input_data):
        try:
            pre_input_data = self.preprocessing(input_data)
            print("Preproccessed data", pre_input_data)
            prediction = self.predict(pre_input_data)  # only one sample
            print("Prediction data", prediction)
            post_prediction = self.postprocessing(prediction)
            print("Processed Prediction data", post_prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return post_prediction
