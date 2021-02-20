from rest_framework import serializers
from .models import Loan_History
from users.models import Clients, LoanOfficer, Loan, AccountUser, Organization
from prediction.models import BehaviouralScores
from prediction.models import  RetentionScores
from prediction.models import  ApplicationScores

class OrganizationSerializer(serializers.ModelSerializer):
	class Meta:
	    model = Organization
	    fields = '__all__'


class ClientsSerializer(serializers.ModelSerializer):
	class Meta:
	    model = Clients
	    fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
	class Meta:
	    model = Loan
	    fields = '__all__'

class LoanOfficerSerializer(serializers.ModelSerializer):
	class Meta:
	    model = LoanOfficer
	    fields = '__all__'

class Loan_HistorySerializer(serializers.ModelSerializer):
	class Meta:
	    model = Loan_History
	    fields = '__all__'


class RetentionScoresSerializer(serializers.ModelSerializer):
	loan = LoanSerializer(many=True, read_only=True, required=False)
	client = ClientsSerializer(many=True, read_only=True, required=False)
	officer = LoanOfficerSerializer(many=True, read_only=True, required=False)
	company = OrganizationSerializer(many=True, read_only=True, required=False)

	
	class Meta:
		model = RetentionScores
		fields = '__all__'


class ApplicationScoresSerializer(serializers.ModelSerializer):
	loan = LoanSerializer(many=True, read_only=True, required=False)
	client = ClientsSerializer(many=True, read_only=True, required=False)
	officer = LoanOfficerSerializer(many=True, read_only=True, required=False)
	company = OrganizationSerializer(many=True, read_only=True, required=False)

		
	
	class Meta:
		model = ApplicationScores
		fields = '__all__'


class BehaviouralScoresSerializer(serializers.ModelSerializer):
	loan = LoanSerializer(many=True, read_only=True, required=False)
	client = ClientsSerializer(many=True, read_only=True, required=False)
	officer = LoanOfficerSerializer(many=True, read_only=True, required=False)
	company = OrganizationSerializer(many=True, read_only=True, required=False)
	
	class Meta:
		model = BehaviouralScores
		fields = '__all__'