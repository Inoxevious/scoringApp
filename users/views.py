from rest_auth.views import (LoginView, LogoutView)
from rest_auth.views import (LoginView, LogoutView, PasswordChangeView)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from .models import *
from rest_framework import status , generics , mixins, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Clients, Loan, LoanOfficer, Organization, AccountUser, Department, Role
from django.http import JsonResponse

# Create your views here.
class APILogoutView(LogoutView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
class APILoginView(LoginView):
    pass

class APIPasswordUpdateView(PasswordChangeView):
    authentication_classes = [TokenAuthentication]

class APICreateUserAPIView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
# We create a token than will be used for future auth
# create auth token
        token = Token.objects.create(user=serializer.instance)
        token_data = {"token": token.key}
        user_role = Role.objects.get(name='manager')
        print('user_role user', user_role)
# create business account
        account_user = AccountUser(user=serializer.instance, user_role=user_role,pushToken=token)
        account_user.save()
        print('accunt user', account_user)

# initialize organization

        qry_organization = Organization(owner=account_user)
        qry_organization.save()
        print('qry_organization user', qry_organization)

# create manager account
        from datetime import datetime, date
        managers_count = Manager.objects.filter(organization=qry_organization).count()
        print('managers_count',managers_count)
        manager_id = 'MFI-{}-DM-{}-{}'.format(qry_organization.id,managers_count,date.today())
        manager_account = Manager(profile=account_user, manager_id= manager_id, organization=qry_organization)
        manager_account.save()
        print('accunt user', manager_account)

        # response_dict = {"user_data": serializer.data,"token_data": token_data }
        token_data = {"token": token.key}

        return Response( {**serializer.data, **token_data},status=status.HTTP_201_CREATED)

class OrganizationAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # serializer = OrganizationSerializer(data=request.data)
    def post(self, request, format=None):
        og_count = Organization.objects.all().count()
        serializer = OrganizationSerializer(data=request.data)
        print('USer',request.user)
        print('Data',request.data)
        if serializer.is_valid():
            account_user = AccountUser.objects.get(user=request.user)
            organization = Organization.objects.get(owner=account_user)
            if organization.orga_id==None :
                from datetime import datetime, date
                organization.orga_id = 'MFI-{}-{}'.format(date.today(),og_count)
                organization.business_name =  request.data.get('business_name')
                organization.business_trading_name =  request.data.get('business_trading_name')
                organization.total_branches =  request.data.get('total_branches')
                organization.address =  request.data.get('address')
                organization.phone =  request.data.get('phone')    
                organization.save()
                print('org id',organization.orga_id )
                # data = OrganizationSerializer(organization, many=True).data
                request.data['orga_id'] = organization.orga_id 
                # data = {"organization":request.data}
                print('Final Data',request.data)
                return Response(request.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # return JsonResponse(data, status = 200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfficerCreate_ListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateUserSerializer
    # serializer = OrganizationSerializer(data=request.data)
    # def post(self, request, format=None):
    #     og_count = Organization.objects.all().count()
    #     serializer = CreateUserSerializer(data=request.data)
    def post(self, request, *args, **kwargs):
        # create user object
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print('USer',request.user)
        print('Data',request.data)
        # Create token
        token = Token.objects.create(user=serializer.instance)
        token_data = {"token": token.key}
        user_role = Role.objects.get(name='officer')
        print('user_role user', user_role)


        
# create system account for new officer
        officer_account = AccountUser(user=serializer.instance, user_role=user_role,pushToken=token)
        officer_account.save()
        print('accunt user', officer_account)

        # get officer organization
        user = AccountUser.objects.get(user=request.user)
        manager_account = Manager.objects.get(profile=user)

        qry_organization = Organization.objects.get(owner=user)
        of_count = LoanOfficer.objects.filter(organization=qry_organization).count()
        if Department.objects.filter(organization=qry_organization,  name='loans').exists():
            officer_department = Department.objects.get(organization=qry_organization, name='loans')
        else:
            officer_department = Department(
                name = 'loans',organization = qry_organization, manager=manager_account
            )
            officer_department.save()
        print('officer department', officer_department)
# create business role account for new officer
        from datetime import datetime, date
        officer_id = 'MFI-{}-LO-{}-{}'.format(qry_organization.id,of_count,date.today())

        officer = LoanOfficer(
                manager = manager_account,

                officer_id = officer_id,
# assign account
                profile =  officer_account,
# assign organization

                organization =  qry_organization,
# assign departmnt
                department =  officer_department,
# assign date of registration
                signup_date =  datetime.today()
        )
        # save officer role object
        officer.save()

        request.data['officer_id'] = officer_id
        # print('Final Data',request.data)
        return Response(request.data, status=status.HTTP_201_CREATED)

class ClientCreate_ListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateUserSerializer
    # serializer = OrganizationSerializer(data=request.data)
    # def post(self, request, format=None):
    #     og_count = Organization.objects.all().count()
    #     serializer = CreateUserSerializer(data=request.data)
    def post(self, request, *args, **kwargs):
        # create user object
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print('USer',request.user)
        print('Data',request.data)
        # Create token
        token = Token.objects.create(user=serializer.instance)
        token_data = {"token": token.key}
        user_role = Role.objects.get(name='client')
        print('user_role user', user_role)


        
# create system account for new officer
        client_account = AccountUser(user=serializer.instance, user_role=user_role,pushToken=token)
        client_account.save()
        print('accunt user', client_account)

        # get officer organization
        user = AccountUser.objects.get(user=request.user)
        signing_officer = LoanOfficer.objects.get(profile=user)

        qry_organization = signing_officer.organization
        lc_count = Clients.objects.filter(organization=qry_organization).count()
        # if Department.objects.filter(organization=qry_organization,  name='loans').exists():
        officer_department = Department.objects.get(organization=qry_organization, name='loans')

        print('officer department', officer_department)
# create business role account for new officer
        from datetime import datetime, date
        client_id = 'MFI-{}-LC-{}-{}'.format(qry_organization.id,lc_count,date.today())

        client = Clients(
                signing_officer = signing_officer,

                client_id = client_id,
# assign account
                profile =  client_account,
# assign organization

                organization =  qry_organization,
# assign departmnt
                department =  officer_department,
# assign date of registration
                registration_date =  datetime.today()
        )
        # save officer role object
        client.save()

        request.data['client_id'] = client_id
        # print('Final Data',request.data)
        return Response(request.data, status=status.HTTP_201_CREATED)

class LoanCreate_ListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateUserSerializer
    # serializer = OrganizationSerializer(data=request.data)
    # def post(self, request, format=None):
    #     og_count = Organization.objects.all().count()
    #     serializer = CreateUserSerializer(data=request.data)
    def post(self, request, *args, **kwargs):
        # create user object
        serializer = LoanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print('USer',request.user)
        print('Data',request.data)

        # get request data
        client_id = request.data.get('client_id')
        # signing_officer_id = request.data.get('signing_officer_id')
        loan_type = request.data.get('loan_type')
        loan_term = request.data.get('loan_term')
        colleteral = request.data.get('colleteral')
        amount= request.data.get('amount')


        client = Clients.objects.get(id=client_id)
        user = AccountUser.objects.get(user=request.user)
        signing_officer = LoanOfficer.objects.get(profile=user)

        qry_organization = signing_officer.organization
        lc_count = Loan.objects.filter(signing_officer__organization=qry_organization).count()
        # if Department.objects.filter(organization=qry_organization,  name='loans').exists():
        officer_department = Department.objects.get(organization=qry_organization, name='loans')

        print('officer department', officer_department)
# create loan
        from datetime import datetime, date
        loan_id = 'MFI-{}-LN-{}-{}'.format(qry_organization.id,lc_count,date.today())

        loan = Loan(
                loan_id = loan_id,
                
# assign lon typ
                loan_type =  loan_type,
# assign ln term
                signing_officer = signing_officer,
                client = client,
                
                application_date =  datetime.today(),
# assign col
                loan_term =  loan_term,
                colleteral =  colleteral,
                amount =  amount
# assign date of application
                
        )
        # save officer role object
        loan.save()

        request.data['loan_id'] = loan_id
        # print('Final Data',request.data)
        return Response(request.data, status=status.HTTP_201_CREATED)



class APIUserListCreateView(generics.ListCreateAPIView):
    """
            create:
                add users
            get:
                Search or get users
                You can search using:
                    :param email
                    :param username
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = AccountUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('email', 'username',)

class APIUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
            get:
                get a specific user
            delete:
                Remove an existing user.
            patch:
                Update one or more fields on an existing user.
            put:
                Update a user.
    """
    queryset = AccountUser.objects.all()
    serializer_class = UserSerializer
