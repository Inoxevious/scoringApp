# Generated by Django 3.0.8 on 2021-02-27 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Endpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('owner', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MLAlgorithm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=1000)),
                ('code', models.CharField(max_length=50000)),
                ('version', models.CharField(max_length=128)),
                ('owner', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parent_endpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prediction.Endpoint')),
            ],
        ),
        migrations.CreateModel(
            name='RetentionScores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_probability', models.FloatField(blank=True, null=True)),
                ('income_color', models.CharField(blank=True, max_length=70, null=True)),
                ('income_text', models.CharField(blank=True, max_length=255, null=True)),
                ('retention_probability', models.FloatField(blank=True, null=True)),
                ('retention_color', models.CharField(blank=True, max_length=70, null=True)),
                ('retention_classification', models.CharField(blank=True, max_length=255, null=True)),
                ('retention_recommendation_process', models.CharField(blank=True, max_length=255, null=True)),
                ('retention_num', models.CharField(blank=True, max_length=255, null=True)),
                ('retention_closure_date', models.CharField(blank=True, max_length=255, null=True)),
                ('retention_client_clv', models.CharField(blank=True, max_length=255, null=True)),
                ('credit_amount', models.FloatField(blank=True, null=True)),
                ('created_by', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_update_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rs_client', to='users.Clients', verbose_name='client')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rs_company', to='users.Organization', verbose_name='company')),
                ('loan_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rs_loan', to='users.Loan', verbose_name='Loan')),
                ('officer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rs_officer', to='users.LoanOfficer', verbose_name='officer')),
            ],
        ),
        migrations.CreateModel(
            name='MLRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_data', models.CharField(max_length=10000)),
                ('full_response', models.CharField(max_length=10000)),
                ('response', models.CharField(max_length=10000)),
                ('feedback', models.CharField(blank=True, max_length=10000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parent_mlalgorithm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prediction.MLAlgorithm')),
            ],
        ),
        migrations.CreateModel(
            name='MLAlgorithmStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=128)),
                ('active', models.BooleanField()),
                ('created_by', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parent_mlalgorithm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status', to='prediction.MLAlgorithm')),
            ],
        ),
        migrations.CreateModel(
            name='BehaviouralScores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_probability', models.FloatField(blank=True, null=True)),
                ('income_color', models.CharField(blank=True, max_length=70, null=True)),
                ('income_text', models.CharField(blank=True, max_length=255, null=True)),
                ('behavioral_probability', models.FloatField(blank=True, null=True)),
                ('behavioral_color', models.CharField(blank=True, max_length=70, null=True)),
                ('behavioral_text', models.CharField(blank=True, max_length=255, null=True)),
                ('behavioral_time_to_default', models.CharField(blank=True, max_length=255, null=True)),
                ('behavioral_contact_channel', models.CharField(blank=True, max_length=255, null=True)),
                ('behavioral_contact_schedule', models.CharField(blank=True, max_length=255, null=True)),
                ('behavioral_message', models.CharField(blank=True, max_length=255, null=True)),
                ('credit_amount', models.FloatField(blank=True, null=True)),
                ('created_by', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_update_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bs_client', to='users.Clients', verbose_name='client')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bs_company', to='users.Organization', verbose_name='company')),
                ('loan_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bs_loan', to='users.Loan', verbose_name='Loan')),
                ('officer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bs_officer', to='users.LoanOfficer', verbose_name='officer')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationScores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_probability', models.FloatField(blank=True, null=True)),
                ('income_color', models.CharField(blank=True, max_length=70, null=True)),
                ('income_text', models.CharField(blank=True, max_length=255, null=True)),
                ('application_probability', models.FloatField(blank=True, null=True)),
                ('application_color', models.CharField(blank=True, max_length=70, null=True)),
                ('application_text', models.CharField(blank=True, max_length=255, null=True)),
                ('credit_amount', models.FloatField(blank=True, null=True)),
                ('created_by', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_update_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='as_client', to='users.Clients', verbose_name='client')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='as_company', to='users.Organization', verbose_name='company')),
                ('loan_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='as_loan', to='users.Loan', verbose_name='Loan')),
                ('officer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='as_officer', to='users.LoanOfficer', verbose_name='officer')),
            ],
        ),
        migrations.CreateModel(
            name='ABTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10000)),
                ('created_by', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('summary', models.CharField(blank=True, max_length=10000, null=True)),
                ('parent_mlalgorithm_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_mlalgorithm_1', to='prediction.MLAlgorithm')),
                ('parent_mlalgorithm_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_mlalgorithm_2', to='prediction.MLAlgorithm')),
            ],
        ),
    ]
