from django.shortcuts import render
# from django.shortcuts import render_to_response
from . import imports as imp
from . import models 

from . import logic as log
# Create your views here.

def importer(request):
    opfile =  '/home/greats/Documents/projects/dreatol/webapp/fintechapp/clean_applications.csv'
    imp.get_data(opfile)
    return render('test.html')

def test(request):
    data = models.loans.objects.all()
    return_data = log.grade_avg(data)
    return render('test.html', {'webdata':return_data})


def dash(request):

    return render("dash.html")

def dashboard(request):
    data = models.loans.objects.all()
    return_data = log.grade_avg(data)
    return render(request, "dashboard-chartsjs.html", {'webdata':return_data})