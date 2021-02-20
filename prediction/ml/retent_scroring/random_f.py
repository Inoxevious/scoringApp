# file backend/server/apps/ml/income_classifier/random_forest.py
# Package Imports
import os
import pandas as pd
import numpy as np
import pickle
import random
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import plot_confusion_matrix, accuracy_score
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
# import xgboost as xgb
import json # will be needed for saving preprocessing details
import joblib 
class RetentionScoring:
    def __init__(self):
        global BASE_DIR, path_to_artifacts
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_to_artifacts = os.path.join(BASE_DIR, 'algo_data/files/')
        # self.model = pickle.load(open(path_to_artifacts + 'light_model.sav', 'rb'))
        self.modelReload = joblib.load(path_to_artifacts + './ra_rf.pkl')
    def preprocessing(self, input_data):
        dataset_columns = [
            'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY',
            'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 
            'DAYS_ID_PUBLISH', 'FLAG_MOBIL', 'FLAG_EMP_PHONE', 'FLAG_WORK_PHONE', 'FLAG_CONT_MOBILE', 'FLAG_PHONE', 'FLAG_EMAIL',
            'OCCUPATION_TYPE', 'CNT_FAM_MEMBERS', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3', 'OBS_30_CNT_SOCIAL_CIRCLE', 
            'DEF_30_CNT_SOCIAL_CIRCLE', 'OBS_60_CNT_SOCIAL_CIRCLE', 'DEF_60_CNT_SOCIAL_CIRCLE', 'DAYS_LAST_PHONE_CHANGE', 
            'FLAG_DOCUMENT_2', 'FLAG_DOCUMENT_3', 'FLAG_DOCUMENT_4', 'FLAG_DOCUMENT_5', 'FLAG_DOCUMENT_6', 'FLAG_DOCUMENT_7', 
            'FLAG_DOCUMENT_8', 'FLAG_DOCUMENT_9', 'FLAG_DOCUMENT_10', 'FLAG_DOCUMENT_11', 'FLAG_DOCUMENT_12', 'FLAG_DOCUMENT_13', 
            'FLAG_DOCUMENT_14', 'FLAG_DOCUMENT_15', 'FLAG_DOCUMENT_16', 'FLAG_DOCUMENT_17', 'FLAG_DOCUMENT_18', 'FLAG_DOCUMENT_19', 
            'FLAG_DOCUMENT_20', 'FLAG_DOCUMENT_21', 'AMT_REQ_CREDIT_BUREAU_HOUR', 'AMT_REQ_CREDIT_BUREAU_DAY', 'AMT_REQ_CREDIT_BUREAU_WEEK', 
            'AMT_REQ_CREDIT_BUREAU_MON', 'AMT_REQ_CREDIT_BUREAU_QRT', 'AMT_REQ_CREDIT_BUREAU_YEAR', 'TARGET'
        ]
        # JSON to pandas DataFrame
        # Set an index, orient = 'index'
        # input_data = input_data.set_index('SK_ID_CURR')
        # print("INdex Data", input_data)
        application_data = pd.DataFrame(input_data, index=[0])
        # application_data = pd.DataFrame.from_dict(input_data)
        # application_data = application_data.json()

        application_data = pd.DataFrame.from_dict(application_data)  
        # print("Un proccessed application_data", application_data)
        # input_data = input_data.set_index('SK_ID_CURR')
        # application_data = pd.read_csv(path_to_artifacts + 'application_train.csv')

        label_vector = application_data['TARGET']
        np.unique(label_vector, return_counts=True)
        # print("INdex Data 2", input_data)

        categorical_features = [
            'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS',
            'NAME_HOUSING_TYPE', 'FLAG_MOBIL', 'FLAG_EMP_PHONE', 'FLAG_WORK_PHONE', 'FLAG_CONT_MOBILE', 'FLAG_PHONE', 'FLAG_EMAIL',
            'OCCUPATION_TYPE', 'EXT_SOURCE_1', 'FLAG_DOCUMENT_2', 'FLAG_DOCUMENT_3', 'FLAG_DOCUMENT_4', 'FLAG_DOCUMENT_5', 
            'FLAG_DOCUMENT_6', 'FLAG_DOCUMENT_7', 'FLAG_DOCUMENT_8', 'FLAG_DOCUMENT_9', 'FLAG_DOCUMENT_10', 'FLAG_DOCUMENT_11', 
            'FLAG_DOCUMENT_12', 'FLAG_DOCUMENT_13', 'FLAG_DOCUMENT_14', 'FLAG_DOCUMENT_15', 'FLAG_DOCUMENT_16', 'FLAG_DOCUMENT_17', 
            'FLAG_DOCUMENT_18', 'FLAG_DOCUMENT_19', 'FLAG_DOCUMENT_20', 'FLAG_DOCUMENT_21'
        ]
        numerical_features = [
            'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 'DAYS_ID_PUBLISH', 'CNT_FAM_MEMBERS', 
            'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3', 'OBS_30_CNT_SOCIAL_CIRCLE', 'DEF_30_CNT_SOCIAL_CIRCLE', 
            'OBS_60_CNT_SOCIAL_CIRCLE', 'DEF_60_CNT_SOCIAL_CIRCLE', 'DAYS_LAST_PHONE_CHANGE', 'AMT_REQ_CREDIT_BUREAU_HOUR', 
            'AMT_REQ_CREDIT_BUREAU_DAY', 'AMT_REQ_CREDIT_BUREAU_WEEK', 'AMT_REQ_CREDIT_BUREAU_MON', 'AMT_REQ_CREDIT_BUREAU_QRT', 
            'AMT_REQ_CREDIT_BUREAU_YEAR'
        ]

        application_data['AMT_ANNUITY'] = application_data['AMT_ANNUITY'].fillna(0)
        application_data['OCCUPATION_TYPE'] = application_data['OCCUPATION_TYPE'].fillna('UNKNOWN')
        application_data['CNT_FAM_MEMBERS'] = application_data['CNT_FAM_MEMBERS'].fillna(0)
        application_data['EXT_SOURCE_1'] = application_data['EXT_SOURCE_1'].fillna(0)
        application_data['EXT_SOURCE_2'] = application_data['EXT_SOURCE_2'].fillna(0)
        application_data['EXT_SOURCE_3'] = application_data['EXT_SOURCE_3'].fillna(0)
        application_data['OBS_30_CNT_SOCIAL_CIRCLE'] = application_data['OBS_30_CNT_SOCIAL_CIRCLE'].fillna(0)
        application_data['DEF_30_CNT_SOCIAL_CIRCLE'] = application_data['DEF_30_CNT_SOCIAL_CIRCLE'].fillna(0)
        application_data['OBS_60_CNT_SOCIAL_CIRCLE'] = application_data['OBS_60_CNT_SOCIAL_CIRCLE'].fillna(0)
        application_data['DEF_60_CNT_SOCIAL_CIRCLE'] = application_data['DEF_60_CNT_SOCIAL_CIRCLE'].fillna(0)
        application_data['DAYS_LAST_PHONE_CHANGE'] = application_data['DAYS_LAST_PHONE_CHANGE'].fillna(3650)
        application_data['AMT_REQ_CREDIT_BUREAU_HOUR'] = application_data['AMT_REQ_CREDIT_BUREAU_HOUR'].fillna(0)
        application_data['AMT_REQ_CREDIT_BUREAU_DAY'] = application_data['AMT_REQ_CREDIT_BUREAU_DAY'].fillna(0)
        application_data['AMT_REQ_CREDIT_BUREAU_WEEK'] = application_data['AMT_REQ_CREDIT_BUREAU_WEEK'].fillna(0)
        application_data['AMT_REQ_CREDIT_BUREAU_MON'] = application_data['AMT_REQ_CREDIT_BUREAU_MON'].fillna(0)
        application_data['AMT_REQ_CREDIT_BUREAU_QRT'] = application_data['AMT_REQ_CREDIT_BUREAU_QRT'].fillna(0)
        application_data['AMT_REQ_CREDIT_BUREAU_YEAR'] = application_data['AMT_REQ_CREDIT_BUREAU_YEAR'].fillna(0)
        treated_dataset = application_data[dataset_columns]


        # sample_class_1 = application_data[application_data['TARGET'] == 1][:20000]
        # sample_class_0 = application_data[application_data['TARGET'] == 0][:20000]
        # treated_dataset = pd.concat([sample_class_1, sample_class_0])[dataset_columns]
        # training_dataset, testing_dataset = train_test_split(treated_dataset, shuffle=True, stratify=treated_dataset['TARGET'])
        # train_mode = dict(training_dataset.mode().iloc[0])
        # train_mode
        features = list(set(dataset_columns) - set(['TARGET'])) 
        # train_features, Y_train = training_dataset[features], training_dataset['TARGET']
        test_features = treated_dataset[features]
       
       
        column_trans = make_column_transformer(
            (OneHotEncoder(), categorical_features),
            (StandardScaler(), numerical_features)
            )
        transformer = column_trans.fit(treated_dataset[features])
       
        # X_train = transformer.transform(train_features)
        clean_data = transformer.transform(test_features)
       
        return clean_data
    # Define a risk assessment function
    def predict(self, input_data):
        # print("PERFORMING PREDICTIONS FOR",input_data)
        prob = self.modelReload.predict_proba(input_data)
        # print("PERFORMING PREDICTIONS DOOONE")
        p = prob.any()
        # print("SENT PREDICTIONS FOR",p)
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
        return {"retention_probability": p, "retention_label": label, "retention_status": "OK"}

    def compute_prediction(self, input_data):
        try:
            
            pre_input_data = self.preprocessing(input_data)
            
            # client_infor = np.array(list(pre_input_data.values())).astype(float)
            # print("Preproccessed data", pre_input_data)
            prediction = self.predict(pre_input_data)  # only one sample
            # print("Prediction data", prediction)
            post_prediction = self.postprocessing(prediction)
            # print("Processed Prediction data", post_prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return post_prediction
