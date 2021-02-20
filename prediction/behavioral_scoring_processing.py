from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from prediction.apps import PredictionConfig
import pandas as pd
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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
    behavioral_prediction ={}
    if  p > 0.67:
        label = "high"
        color = 'red'
        text = 'high risk'
        time = '7 days'
        contact_channel = 'phone'
        contact_schedule = '08/02/2021'
        message = " C'mon, use your brains"
        status = "OK"
        behavioral_prediction["status"] = status
        behavioral_prediction["label"] = label
        behavioral_prediction["behavioral_color"] = color
        behavioral_prediction["behavioral_text"] = text
        behavioral_prediction["behavioral_time_to_default"] = time
        behavioral_prediction["behavioral_contact_channel"] = contact_channel
        behavioral_prediction["behavioral_contact_schedule"] = contact_schedule
        behavioral_prediction["behavioral_message"] = message
    elif  p > 0.33:
        label = "moderate"
        color = 'blue'
        text = 'moderate risk'
        time = '21 days'
        contact_channel = 'phone'
        contact_schedule = '28/02/2021'
        message = " C'mon, use your brains"
        status = "OK"
        behavioral_prediction["status"] = status
        behavioral_prediction["label"] = label
        behavioral_prediction["behavioral_color"] = color
        behavioral_prediction["behavioral_text"] = text
        behavioral_prediction["behavioral_time_to_default"] = time
        behavioral_prediction["behavioral_contact_channel"] = contact_channel
        behavioral_prediction["behavioral_contact_schedule"] = contact_schedule
        behavioral_prediction["behavioral_message"] = message
    else:
        label = "low"
        color = 'green'
        text = 'low risk'
        time = '48 days'
        contact_channel = 'phone'
        contact_schedule = '08/04/2021'
        message = " C'mon, use your brains"
        status = "OK"
        behavioral_prediction["status"] = status
        behavioral_prediction["label"] = label
        behavioral_prediction["behavioral_color"] = color
        behavioral_prediction["behavioral_text"] = text
        behavioral_prediction["behavioral_time_to_default"] = time 
        behavioral_prediction["behavioral_contact_channel"] = contact_channel
        behavioral_prediction["behavioral_contact_schedule"] = contact_schedule
        behavioral_prediction["behavioral_message"] = message

    return behavioral_prediction

def compute_prediction(request):
    try:
        
        # pre_request = self.preprocessing(request)
        # print("Preproccessed data", pre_request)
        score = predict(request)  # only one sample
        print("Prediction data", score)
        post_prediction = postprocessing(score)
        print("Processed Prediction data", post_prediction)
    except Exception as e:
        return {"status": "Error", "message": str(e)}

    return score, post_prediction 