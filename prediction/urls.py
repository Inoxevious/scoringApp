from django.urls import path
import prediction.views as views
# file backend/server/apps/endpoints/urls.py

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import EndpointViewSet
from .views import MLAlgorithmViewSet
from .views import MLRequestViewSet
from .views import PredictView # import PredictView
from .views import ABTestViewSet
from .views import StopABTestView


router = DefaultRouter(trailing_slash=False)
router.register(r"endpoints", EndpointViewSet, basename="endpoints")
router.register(r"mlalgorithms", MLAlgorithmViewSet, basename="mlalgorithms")
router.register(r"mlrequests", MLRequestViewSet, basename="mlrequests")
router.register(r"abtests", ABTestViewSet, basename="abtests")



urlpatterns = [
    url(r"^api/v1/", include(router.urls)),
    # add predict url
    url(
        r"^api/v1/(?P<endpoint_name>.+)/predict$", PredictView.as_view(), name="predict"
    ),

    url(
        r"^api/v1/stop_ab_test/(?P<ab_test_id>.+)", StopABTestView.as_view(), name="stop_ab"
    ),
    path('predict/', views.IRIS_Model_Predict.as_view(), name = 'api_predict'),
    path('app_scoring/', views.LoanApplicationScoringView.as_view(), name = 'api_predict_app_scoring'),
    path('behavioral_scoring/', views.BehavioralScoringView.as_view(), name = 'api_predict_behavioral_scoring'),
    path('retention_scoring/', views.RetentionScoringView.as_view(), name = 'api_predict_retention_scoring'),
]