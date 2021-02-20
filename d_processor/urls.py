from django.conf.urls import url
from django.urls import path, include
from .views import *

# SET THE NAMESPACE!
app_name = 'd_processor'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    # path('all_objects', all_objects, name='all_objects'),
    # path('qs_to_dataset', qs_to_dataset, name='qs_to_dataset'),
    # path('createcsv', createcsv, name='createcsv'),
    # path('qs_to_local_csv', qs_to_local_csv, name='qs_to_local_csv'),
    # path('insert_objects', insert_objects, name='insert_objects'),
    path('import/', importer, name='importer'),
    path('run_predictions/', run_predictions, name='run_predictions'),
    path('add_algo/', add_algo, name='add_algo'),
    path('test/', test, name='test'),
    path('dashboard/', dashboard, name='dashboard'),
]