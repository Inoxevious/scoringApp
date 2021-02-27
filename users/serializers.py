from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Clients, Loan, LoanOfficer, Organization, AccountUser, Department, Manager
from django.contrib.auth.models import User
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password')
#         extra_kwargs = {'password':{'write_only':True}}

#         def create(self, validated_data):
#             user = User(
#                 email=validated_data['email'],
#                 username = validated_data['username'],
#             )
#             user.set_password(validated_data['password'])
#             user.save()
#             Token.objects.create(user=user)
#             return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUser
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name','email')
        write_only_fields = ('password')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active',)

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class AccountUserSerializer(serializers.ModelSerializer):
	class Meta:
	    model = AccountUser
	    fields = ('user_role','user')


class OrganizationSerializer(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(
    #     queryset=AccountUser.objects.all())
    class Meta:
        model = Organization
        fields = '__all__'
        exclude= 'owner'

class DepartmentSerializer(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(
    #     queryset=AccountUser.objects.all())
    class Meta:
        model = Department
        fields = '__all__'


class ManagerSerializer(serializers.ModelSerializer):
    profile = AccountUserSerializer(many=True,read_only=True)
    organization = OrganizationSerializer(many=True,read_only=True)
    department = DepartmentSerializer(many=True,read_only=True)

    class Meta:
        model = Manager
        fields = '__all__'

class LoanOfficerSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(
        queryset=AccountUser.objects.all())
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all())
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all())
    class Meta:
        model = LoanOfficer
        fields = ('officer_id','profile','organization','department')
        read_only_fields = ('id','officer_id',)
        
class ClientsSerializer(serializers.ModelSerializer):
    account = AccountUserSerializer(many=True, read_only=True, required=False)
    company = OrganizationSerializer(many=True, read_only=True, required=False)
    officer = LoanOfficerSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Clients
        fields = '__all__'
class LoanSerializer(serializers.ModelSerializer):
	class Meta:
	    model = Loan
	    fields = '__all__'
        
