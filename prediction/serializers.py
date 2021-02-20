from rest_framework import serializers
from users.models import Clients, LoanOfficer, Loan, AccountUser, Organization
from .models import BehaviouralScores
from .models import  RetentionScores
from .models import  ApplicationScores


# backend/server/apps/endpoints/serializers.py file
from rest_framework import serializers
from .models import Endpoint
from .models import MLAlgorithm
from .models import MLAlgorithmStatus
from .models import MLRequest
from .models import ABTest


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        read_only_fields = ("id", "name", "owner", "created_at")
        fields = read_only_fields


class MLAlgorithmSerializer(serializers.ModelSerializer):

    current_status = serializers.SerializerMethodField(read_only=True)

    def get_current_status(self, mlalgorithm):
        return MLAlgorithmStatus.objects.filter(parent_mlalgorithm=mlalgorithm).latest('created_at').status

    class Meta:
        model = MLAlgorithm
        read_only_fields = ("id", "name", "description", "code",
                            "version", "owner", "created_at",
                            "parent_endpoint", "current_status")
        fields = read_only_fields

class MLAlgorithmStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAlgorithmStatus
        read_only_fields = ("id", "active")
        fields = ("id", "active", "status", "created_by", "created_at",
                            "parent_mlalgorithm")

class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        read_only_fields = (
            "id",
            "input_data",
            "full_response",
            "response",
            "created_at",
            "parent_mlalgorithm",
        )
        fields =  (
            "id",
            "input_data",
            "full_response",
            "response",
            "feedback",
            "created_at",
            "parent_mlalgorithm",
        )

# please add at the end of file backend/server/apps/endpoints/serializers.py
class ABTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABTest
        read_only_fields = (
            "id",
            "ended_at",
            "created_at",
            "summary",
        )
        fields = (
            "id",
            "title",
            "created_by",
            "created_at",
            "ended_at",
            "summary",
            "parent_mlalgorithm_1",
            "parent_mlalgorithm_2",
            )




class RetentionScoresSerializer(serializers.ModelSerializer):
	class Meta:
		model = RetentionScores
		fields = '__all__'


class ApplicationScoresSerializer(serializers.ModelSerializer):

	
	class Meta:
		model = ApplicationScores
		fields = '__all__'


class BehaviouralScoresSerializer(serializers.ModelSerializer):
	class Meta:
		model = BehaviouralScores
		fields = '__all__'