from django.conf.urls import url
from django.urls import path, include
from . import views 
# from .views import *
# SET THE NAMESPACE!
app_name = 'companies'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    # path("loan_history_listing/", views.Loan_HistoryListing.as_view(), name = 'listing'),
    url(r'^api/v1.0/application_scoring', views.ApplicationAPIView.as_view(), name='application_scoring_view'),
    url(r'^api/v1.0/behavioral_scoring', views.BehavioralAPIView.as_view(), name='behavioral_scoring_view'),
    url(r'^api/v1.0/retention_scoring', views.RetentionAPIView.as_view(), name='retention_scoring_view'),
    # url(r'^api/v1.0/retention_scoring[/]?$', views.RetentionAPIView.as_view(), name='retention_scoring_view'),
    path("ajax/business/", views.getBusiness, name = 'get_businesses'),
    path("ajax/mortage/", views.getMortage, name = 'get_mortages'),
    path("ajax/school/", views.getSchool, name = 'get_schools'),
    path("ajax/funeral/", views.getFuneral, name = 'get_funerals'),
    path('data_for_charts', views.data_for_charts, name="data_for_charts"),
    path('data_aggretation', views.data_aggretation, name="data_aggretation"),
    path('index/$', views.HomeView.as_view(), name="index"),
    path('', views.Index.as_view(), name='index'),


    path('income_classifier/', views.ApplicationAnalyticsResultsView.as_view(), name="income_classifier"),    
    path('application_analytics/', views.ApplicationAnalyticsResultsView.as_view(), name='application_analytics'),
    path('retention_analytics/', views.RetentionAnalyticsResultsView.as_view(), name='retention_analytics'),
    path('behavioral_analytics/', views.BehavioralAnalyticsResultsView.as_view(), name='behavioral_analytics'),
    path('client_profile/', views.client_profile, name='client_profile'),
    path('application_report/', views.application_report, name='application_report'),
    path('application_report_export_csv/', views.application_report_export_csv, name='application_report_export_csv'),
    path('officer_profile/', views.officer_profile, name='officer_profile'),
    path('live_app_score_pred/', views.live_app_score_pred, name='live_app_score_pred'),

    path('reports/', views.reports, name='reports'),
    path('articles/', views.articles, name='articles'),
   
]