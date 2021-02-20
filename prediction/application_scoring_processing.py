from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from prediction.apps import PredictionConfig
import pandas as pd
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from prediction.ml.application_classifier.scoring_model import LoanApplicationScoring

# class GetApplicationScore:

#     def __init__(self):
#         global  prediction

def predict(request):
    data = request.data
    keys = []
    values = []
    for key in data:
        keys.append(key)
        values.append(data[key])
    X = pd.Series(values).to_numpy().reshape(1, -1)
    loaded_mlmodel = PredictionConfig.applicationscoringmodel
    y_pred = loaded_mlmodel.predict_proba(X)[:,-1]
    print(y_pred)
    y_pred = pd.Series(y_pred)
    return y_pred[0]
def postprocessing(p):
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


def compute_prediction(request):
    try:
        
        # pre_request = self.preprocessing(request)
        # print("Preproccessed data", pre_request)
        prediction = predict(request)  # only one sample
        print("Prediction data", prediction)
        post_prediction = postprocessing(prediction)
        print("Processed Prediction data", post_prediction)
    except Exception as e:
        return {"status": "Error", "message": str(e)}

    return post_prediction