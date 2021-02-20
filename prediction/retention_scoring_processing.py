from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from prediction.apps import PredictionConfig
import pandas as pd
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

def preprocessing(input_data):
    values_fill_missing = PredictionConfig.retention_values_fill_missing 
    encoders =  PredictionConfig.retention_encoders
    # JSON to pandas DataFrame
    
    input_data = pd.DataFrame(input_data, index=[0])
    # fill missing values
    input_data.fillna(values_fill_missing)
    # convert categoricals
    for column in [
        "workclass",
        "education",
        "marital-status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "native-country",
    ]:
        categorical_convert = encoders[column]
        input_data[column] = categorical_convert.transform(input_data[column])

    return input_data

def predict(input_data):
    loaded_mlmodel = PredictionConfig.retention_model
    y_pred = loaded_mlmodel.predict_proba(input_data)
    return  y_pred[0]


def postprocessing(retention_prediction):
    predict_dict_data = {}
    if  retention_prediction['income_probability'] > 0.67:
        loan_num = 3
        closure_date = '28/02/2021'
        client_clv = "20"
        color = 'red'
        recommendation_process = "Reject client"
        classification = 'Reject'
        retention_prediction["retention_classification"] = classification                
        retention_prediction["retention_loan_num"] = loan_num
        retention_prediction["retention_closure_date"] = closure_date
        retention_prediction["retention_client_clv"] = client_clv
        retention_prediction["retention_color"] = color
        retention_prediction["retention_probability"] = retention_prediction['income_probability']

        retention_prediction["retention_recommendation_process"] = recommendation_process
    elif  retention_prediction['income_probability'] > 0.33:
        loan_num = 3
        closure_date = '28/02/2021'
        client_clv = "1100"
        color = 'blue'
        recommendation_process = "Visit business and home"
        classification = 'More detailed'
        retention_prediction["retention_classification"] = classification                
        retention_prediction["retention_loan_num"] = loan_num
        retention_prediction["retention_closure_date"] = closure_date
        retention_prediction["retention_client_clv"] = client_clv
        retention_prediction["retention_color"] = color
        retention_prediction["retention_probability"] = retention_prediction['income_probability']
        retention_prediction["retention_recommendation_process"] = recommendation_process
    else:
        loan_num = 3
        closure_date = '28/02/2021'
        client_clv = "2000"
        color = 'green'
        recommendation_process = "Automatic approval"
        classification = 'Pre-Approved'
        retention_prediction["retention_classification"] = classification                
        retention_prediction["retention_loan_num"] = loan_num
        retention_prediction["retention_closure_date"] = closure_date
        retention_prediction["retention_client_clv"] = client_clv
        retention_prediction["retention_color"] = color
        retention_prediction["retention_probability"] = retention_prediction['income_probability']
        retention_prediction["retention_recommendation_process"] = recommendation_process

    return retention_prediction

def compute_prediction(prediction):
    try:
        # input_data = preprocessing(input_data)
        # prediction = predict(input_data)[0]  # only one sample
        prediction = postprocessing(prediction)
    except Exception as e:
        return {"status": "Error", "message": str(e)}

    return prediction