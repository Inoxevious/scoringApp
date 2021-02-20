from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from prediction.apps import PredictionConfig
import pandas as pd
from prediction.ml.income_classifier.random_forest import RandomForestClassifier

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from prediction.ml.application_classifier.scoring_model import LoanApplicationScoring
from prediction.application_scoring_processing import compute_prediction as app_scoring
from prediction.behavioral_scoring_processing import compute_prediction as behavioral_scoring
from prediction.retention_scoring_processing import compute_prediction as retention_scoring
from prediction.serializers import *

# backend/server/apps/endpoints/views.py file
from rest_framework import viewsets
from rest_framework import mixins

from .models import Endpoint
from .serializers import EndpointSerializer

from .models import MLAlgorithm
from .serializers import MLAlgorithmSerializer

from .models import MLAlgorithmStatus
from .serializers import MLAlgorithmStatusSerializer

from .models import MLRequest
from .serializers import MLRequestSerializer

import json
from numpy.random import rand
from rest_framework import views, status
from rest_framework.response import Response
from prediction.ml.registry import MLRegistry
from django.db import transaction
from .models import ABTest
from .serializers import ABTestSerializer
from prediction.ml.income_classifier.random_forest import RandomForestClassifier
from prediction.ml.income_classifier.extra_trees import ExtraTreesClassifier
from prediction.ml.application_classifier.random_forest import RandomForestApplicationClassifier
from prediction.ml.application_classifier.random_f import LoanApplicationClassifier
from prediction.ml.application_classifier.scoring_model import LoanApplicationScoring

# please add to the file backend/server/apps/endpoints/views.py

from django.db.models import F
import datetime
class EndpointViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.all()


class MLAlgorithmViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = MLAlgorithmSerializer
    queryset = MLAlgorithm.objects.all()


def deactivate_other_statuses(instance):
    old_statuses = MLAlgorithmStatus.objects.filter(parent_mlalgorithm = instance.parent_mlalgorithm,
                                                        created_at__lt=instance.created_at,
                                                        active=True)
    for i in range(len(old_statuses)):
        old_statuses[i].active = False
    MLAlgorithmStatus.objects.bulk_update(old_statuses, ["active"])

class MLAlgorithmStatusViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.CreateModelMixin
):
    serializer_class = MLAlgorithmStatusSerializer
    queryset = MLAlgorithmStatus.objects.all()
    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(active=True)
                # set active=False for other statuses
                deactivate_other_statuses(instance)



        except Exception as e:
            raise APIException(str(e))

class MLRequestViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.UpdateModelMixin
):
    serializer_class = MLRequestSerializer
    queryset = MLRequest.objects.all()

class PredictView(views.APIView):
    def post(self, request, endpoint_name, format=None):

        algorithm_status = self.request.query_params.get("status", "production")
        algorithm_version = self.request.query_params.get("version")
        all_ags = MLAlgorithm.objects.all()
        print("Req end name",all_ags)
        print("FILTERING STARTS")
        print("Req end name",endpoint_name)
        print("Req status name",algorithm_status)

        # algs = MLAlgorithm.objects.filter(parent_endpoint__name = endpoint_name)
        # print("ALgo object 1st filter",algs)

        # algorithm_object = registry.endpoints[algs[alg_index].id]
        # prediction = algorithm_object.compute_prediction(request.data)
        algorithm_object = object()
        if endpoint_name == 'income_classifier':
            algorithm_object = RandomForestClassifier()

        elif endpoint_name == 'loan_application_scoring':
            algorithm_object = LoanApplicationScoring()

        elif endpoint_name == 'loan_application_classifier':
            algorithm_object = LoanApplicationClassifier()
            
        print("PREDICTIOON OBJECT",algorithm_object)
        prediction = algorithm_object.compute_prediction(request.data)
        print("PREDICTIOON RES",prediction)
        algs = MLAlgorithm.objects.get(parent_endpoint__name = endpoint_name)

        label = prediction["label"] if "label" in prediction else "error"
        ml_request = MLRequest(
            input_data=json.dumps(request.data),
            full_response=prediction,
            response=label,
            feedback="",
            parent_mlalgorithm=algs,
        )
        ml_request.save()

        prediction["request_id"] = ml_request.id

        return Response(prediction)



class ABTestViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.CreateModelMixin, mixins.UpdateModelMixin
):
    serializer_class = ABTestSerializer
    queryset = ABTest.objects.all()

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save()
                # update status for first algorithm

                status_1 = MLAlgorithmStatus(status = "ab_testing",
                                created_by=instance.created_by,
                                parent_mlalgorithm = instance.parent_mlalgorithm_1,
                                active=True)
                status_1.save()
                deactivate_other_statuses(status_1)
                # update status for second algorithm
                status_2 = MLAlgorithmStatus(status = "ab_testing",
                                created_by=instance.created_by,
                                parent_mlalgorithm = instance.parent_mlalgorithm_2,
                                active=True)
                status_2.save()
                deactivate_other_statuses(status_2)

        except Exception as e:
            raise APIException(str(e))

class StopABTestView(views.APIView):
    def post(self, request, ab_test_id, format=None):

        try:
            ab_test = ABTest.objects.get(pk=ab_test_id)

            if ab_test.ended_at is not None:
                return Response({"message": "AB Test already finished."})

            date_now = datetime.datetime.now()
            # alg #1 accuracy
            all_responses_1 = MLRequest.objects.filter(parent_mlalgorithm=ab_test.parent_mlalgorithm_1, created_at__gt = ab_test.created_at, created_at__lt = date_now).count()
            correct_responses_1 = MLRequest.objects.filter(parent_mlalgorithm=ab_test.parent_mlalgorithm_1, created_at__gt = ab_test.created_at, created_at__lt = date_now, response=F('feedback')).count()
            accuracy_1 = correct_responses_1 / float(all_responses_1)
            print(all_responses_1, correct_responses_1, accuracy_1)

            # alg #2 accuracy
            all_responses_2 = MLRequest.objects.filter(parent_mlalgorithm=ab_test.parent_mlalgorithm_2, created_at__gt = ab_test.created_at, created_at__lt = date_now).count()
            correct_responses_2 = MLRequest.objects.filter(parent_mlalgorithm=ab_test.parent_mlalgorithm_2, created_at__gt = ab_test.created_at, created_at__lt = date_now, response=F('feedback')).count()
            accuracy_2 = correct_responses_2 / float(all_responses_2)
            print(all_responses_2, correct_responses_2, accuracy_2)

            # select algorithm with higher accuracy
            alg_id_1, alg_id_2 = ab_test.parent_mlalgorithm_1, ab_test.parent_mlalgorithm_2
            # swap
            if accuracy_1 < accuracy_2:
                alg_id_1, alg_id_2 = alg_id_2, alg_id_1

            status_1 = MLAlgorithmStatus(status = "production",
                            created_by=ab_test.created_by,
                            parent_mlalgorithm = alg_id_1,
                            active=True)
            status_1.save()
            deactivate_other_statuses(status_1)
            # update status for second algorithm
            status_2 = MLAlgorithmStatus(status = "testing",
                            created_by=ab_test.created_by,
                            parent_mlalgorithm = alg_id_2,
                            active=True)
            status_2.save()
            deactivate_other_statuses(status_2)


            summary = "Algorithm #1 accuracy: {}, Algorithm #2 accuracy: {}".format(accuracy_1, accuracy_2)
            ab_test.ended_at = date_now
            ab_test.summary = summary
            ab_test.save()

        except Exception as e:
            return Response({"status": "Error", "message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"message": "AB Test finished.", "summary": summary})

# Create your views here.
# Class based view to predict based on IRIS model
class IRIS_Model_Predict(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        data = request.data
        keys = []
        values = []
        for key in data:
            keys.append(key)
            values.append(data[key])
        X = pd.Series(values).to_numpy().reshape(1, -1)
        loaded_mlmodel = PredictionConfig.irismlmodel
        y_pred = loaded_mlmodel.predict(X)
        y_pred = pd.Series(y_pred)
        target_map = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
        y_pred = y_pred.map(target_map).to_numpy()
        response_dict = {"Prediced Iris Species": y_pred[0]}
        print(response_dict)
        return Response(response_dict, status=200)

class LoanApplicationScoringView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        data = request.data
        print(data)
        score = app_scoring(request)
        print(score)
        return Response(score, status=200)

    def get(self, request):
        global qry
        queryList = ApplicationScores.objects.all()
        loan_officer = self.request.query_params.get('loan_officer', None)
        sort_by = self.request.query_params.get('sort_by', None)

        if loan_officer:
            queryList = ApplicationScores.objects.filter(loan_officer = loan_officer)[:5]
  
        # sort it if applied on based on price/points
        if sort_by == "income":
            queryList = queryList.order_by("client_id")
        elif sort_by == "credit_amount":
            queryList = queryList.order_by("loan_amount")

        # get predictions for applications scoring predictions
        data = ApplicationScoresSerializer(queryList, many=True).data
        return Response(data, status=200)

        

class BehavioralScoringView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        data = request.data
        print(data)
        score, post_prediction = behavioral_scoring(request)
        print(post_prediction)
        return Response(post_prediction, status=200)


    def get(self, request):
        serializer_class = BehaviouralScoresSerializer
        # filter the queryset based on the filters applied
        global qry
        queryList = BehaviouralScores.objects.all()
        loan_officer = self.request.query_params.get('loan_officer', None)
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
        return Response(data, status=200) 

class RetentionScoringView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        data = request.data
        print(data)
        algorithm_object = RandomForestClassifier()
        # print("PREDICTIOON OBJECT",algorithm_object)
        prediction = algorithm_object.compute_prediction(request.data)
        # score = retention_scoring(request.data)
        post_processing = retention_scoring(prediction)
        print(post_processing)
        return Response(post_processing, status=200)

    def get(self, request):
        serializer_class = RetentionScoresSerializer
        # filter the queryset based on the filters applied
        global qry
        queryList = RetentionScores.objects.all()
        loan_officer = self.request.query_params.get('loan_officer', None)
        sort_by = self.request.query_params.get('sort_by', None)

        if loan_officer:
            queryList = RetentionScores.objects.filter(loan_officer = loan_officer)[:5]
  
        # sort it if applied on based on price/points
        if sort_by == "income":
            queryList = queryList.order_by("client_id")
        elif sort_by == "credit_amount":
            queryList = queryList.order_by("loan_amount")
        # get predictions for applications scoring predictions
        data = RetentionScoresSerializer(queryList, many=True).data
        data = {"retention_data":data}
        return  Response(data,status=200)