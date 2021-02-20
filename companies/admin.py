from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass

@admin.register(IncomeData)
class IncomeDataAdmin(admin.ModelAdmin):
    pass

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    pass

