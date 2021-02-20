from django.db import models
from users.models import Clients, LoanOfficer, Loan, Organization

class Endpoint(models.Model):
    '''
    The Endpoint object represents ML API endpoint.

    Attributes:
        name: The name of the endpoint, it will be used in API URL,
        owner: The string with owner name,
        created_at: The date when endpoint was created.
    '''
    name = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

class MLAlgorithm(models.Model):
    '''
    The MLAlgorithm represent the ML algorithm object.

    Attributes:
        name: The name of the algorithm.
        description: The short description of how the algorithm works.
        code: The code of the algorithm.
        version: The version of the algorithm similar to software versioning.
        owner: The name of the owner.
        created_at: The date when MLAlgorithm was added.
        parent_endpoint: The reference to the Endpoint.
    '''
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    code = models.CharField(max_length=50000)
    version = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)

class MLAlgorithmStatus(models.Model):
    '''
    The MLAlgorithmStatus represent status of the MLAlgorithm which can change during the time.

    Attributes:
        status: The status of algorithm in the endpoint. Can be: testing, staging, production, ab_testing.
        active: The boolean flag which point to currently active status.
        created_by: The name of creator.
        created_at: The date of status creation.
        parent_mlalgorithm: The reference to corresponding MLAlgorithm.

    '''
    status = models.CharField(max_length=128)
    active = models.BooleanField()
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE, related_name = "status")

class MLRequest(models.Model):
    '''
    The MLRequest will keep information about all requests to ML algorithms.

    Attributes:
        input_data: The input data to ML algorithm in JSON format.
        full_response: The response of the ML algorithm.
        response: The response of the ML algorithm in JSON format.
        feedback: The feedback about the response in JSON format.
        created_at: The date when request was created.
        parent_mlalgorithm: The reference to MLAlgorithm used to compute response.
    '''
    input_data = models.CharField(max_length=10000)
    full_response = models.CharField(max_length=10000)
    response = models.CharField(max_length=10000)
    feedback = models.CharField(max_length=10000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE)
# please add at the end of file backend/server/apps/endpoints/models.py
# please add at the end of file backend/server/apps/endpoints/models.py

class ABTest(models.Model):
    '''
    The ABTest will keep information about A/B tests.
    Attributes:
        title: The title of test.
        created_by: The name of creator.
        created_at: The date of test creation.
        ended_at: The date of test stop.
        summary: The description with test summary, created at test stop.
        parent_mlalgorithm_1: The reference to the first corresponding MLAlgorithm.
        parent_mlalgorithm_2: The reference to the second corresponding MLAlgorithm.
    '''
    title = models.CharField(max_length=10000)
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    summary = models.CharField(max_length=10000, blank=True, null=True)

    parent_mlalgorithm_1 = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE, related_name="parent_mlalgorithm_1",blank=True, null=True)
    parent_mlalgorithm_2 = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE, related_name="parent_mlalgorithm_2",blank=True, null=True)



class ApplicationScores(models.Model):
    loan_id = models.ForeignKey(Loan, related_name="as_loan", verbose_name="Loan", on_delete = models.CASCADE,null=True, blank=True)
    officer = models.ForeignKey(LoanOfficer, related_name="as_officer", verbose_name="officer", on_delete = models.CASCADE,null=True, blank=True)
    client = models.ForeignKey(Clients, related_name="as_client", verbose_name="client", on_delete = models.CASCADE,null=True, blank=True)
    company = models.ForeignKey(Organization, related_name="as_company", verbose_name="company", on_delete = models.CASCADE,null=True, blank=True)
    income_probability = models.FloatField(null=True ,blank=True)
    income_color = models.CharField(null=True ,blank=True,max_length=70)
    income_text = models.CharField(null=True ,blank=True,max_length=255)
    application_probability = models.FloatField(null=True ,blank=True)
    application_color = models.CharField(null=True ,blank=True,max_length=70)
    application_text = models.CharField(null=True ,blank=True,max_length=255)
    credit_amount = models.FloatField(null=True ,blank=True)
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_update_at = models.DateTimeField(auto_now_add=True, blank=True)
    # def __str__(self):
    #     return self.client


class BehaviouralScores(models.Model):
    loan_id = models.ForeignKey(Loan, related_name="bs_loan", verbose_name="Loan", on_delete = models.CASCADE,null=True, blank=True)
    officer = models.ForeignKey(LoanOfficer, related_name="bs_officer", verbose_name="officer", on_delete = models.CASCADE,null=True, blank=True)
    client = models.ForeignKey(Clients, related_name="bs_client", verbose_name="client", on_delete = models.CASCADE,null=True, blank=True)
    company = models.ForeignKey(Organization, related_name="bs_company", verbose_name="company", on_delete = models.CASCADE,null=True, blank=True)
    income_probability = models.FloatField(null=True ,blank=True)
    income_color = models.CharField(null=True ,blank=True,max_length=70)
    income_text = models.CharField(null=True ,blank=True,max_length=255)
    behavioral_probability = models.FloatField(null=True ,blank=True)
    behavioral_color = models.CharField(null=True ,blank=True,max_length=70)
    behavioral_text = models.CharField(null=True ,blank=True,max_length=255)
    behavioral_time_to_default  = models.CharField(null=True ,blank=True,max_length=255)
    behavioral_contact_channel  = models.CharField(null=True ,blank=True,max_length=255)
    behavioral_contact_schedule  = models.CharField(null=True ,blank=True,max_length=255)
    behavioral_message  = models.CharField(null=True ,blank=True,max_length=255)
    credit_amount = models.FloatField(null=True ,blank=True)
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_update_at = models.DateTimeField(auto_now_add=True, blank=True)
    # def __str__(self):
    #     return self.client

class RetentionScores(models.Model):
    loan_id = models.ForeignKey(Loan, related_name="rs_loan", verbose_name="Loan", on_delete = models.CASCADE,null=True, blank=True)
    officer = models.ForeignKey(LoanOfficer, related_name="rs_officer", verbose_name="officer", on_delete = models.CASCADE,null=True, blank=True)
    client = models.ForeignKey(Clients, related_name="rs_client", verbose_name="client", on_delete = models.CASCADE,null=True, blank=True)
    company = models.ForeignKey(Organization, related_name="rs_company", verbose_name="company", on_delete = models.CASCADE,null=True, blank=True)
    income_probability = models.FloatField(null=True ,blank=True)
    income_color = models.CharField(null=True ,blank=True,max_length=70)
    income_text = models.CharField(null=True ,blank=True,max_length=255)
    retention_probability = models.FloatField(null=True ,blank=True)
    retention_color = models.CharField(null=True ,blank=True,max_length=70)
    retention_classification = models.CharField(null=True ,blank=True,max_length=255)
    retention_recommendation_process  = models.CharField(null=True ,blank=True,max_length=255)
    retention_num  = models.CharField(null=True ,blank=True,max_length=255)
    retention_closure_date = models.CharField(null=True ,blank=True,max_length=255)
    retention_client_clv  = models.CharField(null=True ,blank=True,max_length=255)
    credit_amount = models.FloatField(null=True ,blank=True)
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_update_at = models.DateTimeField(auto_now_add=True, blank=True)
    # def __str__(self):
    #     return self.client