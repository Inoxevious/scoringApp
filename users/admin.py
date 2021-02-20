from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(AccountUser)
class AccountUserAdmin(admin.ModelAdmin):
    pass


@admin.register(LoanOfficer)
class LoanOfficerAdmin(admin.ModelAdmin):
    pass

@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    pass


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    pass


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    pass