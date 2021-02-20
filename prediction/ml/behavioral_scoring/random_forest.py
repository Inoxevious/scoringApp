# file backend/server/apps/ml/income_classifier/random_forest.py
# Package Imports
import pickle
import pandas as pd
import numpy as np
from sklearn import preprocessing
import joblib
import pandas as pd
import os
from sklearn.preprocessing import PolynomialFeatures
class RandomForestApplicationClassifier:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_to_artifacts = os.path.join(BASE_DIR, 'algo_data/files/')
        self.model = pickle.load(open(path_to_artifacts + 'light_model.sav', 'rb'))

    def preprocessing(self, input_data):
        # JSON to pandas DataFrame
        # Set an index
        # input_data = input_data.set_index('SK_ID_CURR')
        # print("INdex Data", input_data)
        input_data = pd.DataFrame(input_data, index=[0])
        print("INdex Data 2", input_data)

        # Subset numerical data
        numerics = ['int16','int32','int64','float16','float32','float64']
        numerical_vars = list(input_data.select_dtypes(include=numerics).columns)
        numerical_data = input_data[numerical_vars]
        # fill missing values
        # Fill in missing values
        numerical_data = numerical_data.fillna(numerical_data.mean())
        print("numerical_data", numerical_data)
        # input_data.fillna(self.values_fill_missing)
        # convert categoricals
        # Subset categorical data
        cates = ['object']
        cate_vars = list(input_data.select_dtypes(include=cates).columns)
        categorical_data = input_data[cate_vars]
        # Fill in missing values
        categorical_data = categorical_data.fillna(method = 'ffill')

        # Instantiate label encoder
        le = preprocessing.LabelEncoder()
        categorical_data = categorical_data.apply(lambda col: le.fit_transform(col).astype(str))
        categorical_data
        print("categorical_data", categorical_data)
        # Concat the data
        clean_data = pd.concat([categorical_data, numerical_data], axis = 1)
        print("clean_data", clean_data)

        # if clean_data['TARGET']:
            # Prepare test data for individual predictions
        clean_data = clean_data.drop(['TARGET'], axis = 1)
        print("final clean_data", clean_data)
        return clean_data
    # Define a risk assessment function
    def predict(self, input_data):
        
          #Subset a specific client infor, *a* represent SK_ID_CURR
        # client_infor = np.array(list(input_data.values())).astype(float)
        prob = self.model.predict_proba(input_data)    #predict a client's probability of defaulting
        p = prob[1]
        return p
   # def predict(self, input_data):
    #     return self.model.predict_proba(input_data)

    def postprocessing(self, p):
        label = "low"
        print("Prob",p)
        if p > 0.67:
            label = "high"
            # print('Client with ID # {} has a high risk of defaulting the loan'.format(a))
        elif p > 0.33:
            label = "high"
            # print('Client with ID # {} has a moderate risk of defaulting the loan'.format(a))
        else:
            label = "low"
            # print('Client with ID # {} has a low risk of defaulting the loan'.format(a))
        print("probability:",p, "label:", label, "status:", "OK")    
        return {"probability": p, "label": label, "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            print("Un proccessed data", input_data)
            pre_input_data = self.preprocessing(input_data)
            # client_infor = pre_input_data
            client_infor = np.array(list(pre_input_data.values())).astype(float)
            print("Preproccessed data", client_infor)
            prediction = self.predict(client_infor)[0]  # only one sample
            print("Prediction data", pre_input_data)
            post_prediction = self.postprocessing(prediction)
            print("Processed Prediction data", post_prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction
