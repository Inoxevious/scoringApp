from django.urls import path, include
from users.views import *
from django.conf.urls import url
urlpatterns = [
    path('users/', APIUserListCreateView.as_view(), name='users_list'),
    path('organizationcreate_list/', OrganizationAPIView.as_view(), name='organizationcreate_list'),
    path('officercreate_list/', OfficerCreate_ListAPIView.as_view(), name='officercreate_list'),
    path('loancreate_list/', LoanCreate_ListAPIView.as_view(), name='loancreate_list'),
    path('clientcreate_list/', ClientCreate_ListAPIView.as_view(), name='clientcreate_list'),
    path('user/<int:pk>/',  APIUserDetailView.as_view(), name='user_detail'),
    path('register/',APICreateUserAPIView.as_view(),name='auth_user_create'),
    path('login/', APILoginView.as_view(), name='api_login'),
    path('logout/', APILogoutView.as_view(), name='api_logout'),
    path('update_password/', APIPasswordUpdateView.as_view(), name='api_update_password'),
    # path('organizationcreate_list/',organizationcreate_list, name='organizationcreate_list'),


]