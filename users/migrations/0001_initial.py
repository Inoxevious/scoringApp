# Generated by Django 3.0.8 on 2021-02-27 00:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.UserManager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=70, null=True)),
                ('work_email', models.CharField(blank=True, max_length=70, null=True)),
                ('personal_email', models.CharField(blank=True, max_length=70, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('accepted_terms', models.BooleanField(default=False)),
                ('home_address', models.TextField(blank=True, null=True)),
                ('date_birth', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=70, null=True)),
                ('id_number', models.CharField(blank=True, max_length=20, null=True)),
                ('gender', models.CharField(blank=True, max_length=20, null=True)),
                ('education_level', models.CharField(blank=True, max_length=70, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=20, null=True)),
                ('number_dependants', models.IntegerField(blank=True, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='staticfiles/images')),
                ('facebookId', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('android', models.BooleanField(blank=True, default=False)),
                ('ios', models.NullBooleanField(default=False)),
                ('acceptPush', models.BooleanField(default=False)),
                ('pushToken', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', users.UserManager.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('registration_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('mission', models.TextField(blank=True, null=True)),
                ('vision', models.TextField(blank=True, null=True)),
                ('statement', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/%Y/%m/%d')),
                ('video', models.FileField(blank=True, null=True, upload_to='media/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('client', 'client'), ('owner', 'owner'), ('officer', 'officer'), ('manager', 'manager'), ('admin', 'admin')], default='officer', max_length=70)),
                ('user_group', models.CharField(choices=[('client', 'client'), ('executive', 'executive'), ('field_officer', 'field_officer'), ('internal_officer', 'internal_officer')], default='field_officer', max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orga_id', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('business_name', models.CharField(blank=True, max_length=70, null=True)),
                ('business_trading_name', models.CharField(blank=True, max_length=70, null=True)),
                ('total_branches', models.IntegerField(blank=True, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='staticfiles/images')),
                ('address', models.TextField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=70, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='media/%Y/%m/%d')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='media/%Y/%m/%d')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='media/%Y/%m/%d')),
                ('statement', models.TextField(blank=True, null=True)),
                ('acceptPush', models.BooleanField(default=False)),
                ('pushToken', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization', to='users.AccountUser', verbose_name='Micro Finance Director')),
                ('registered_byuser_as', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Role', verbose_name='Admin')),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_id', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('signup_date', models.DateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Organization')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manager', to='users.AccountUser', verbose_name='Manager Account')),
            ],
        ),
        migrations.CreateModel(
            name='LoanOfficer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('officer_id', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('signup_date', models.DateTimeField()),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Department')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Manager', verbose_name='Manager')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Organization')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='officer', to='users.AccountUser', verbose_name='Officer Account')),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_id', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('loan_type', models.CharField(choices=[('business', 'business'), ('school_fees', 'school_fees'), ('mortage', 'mortage'), ('funeral_assistance', 'funeral_assistance')], default='school_fees', max_length=70)),
                ('application_date', models.DateTimeField(blank=True, null=True)),
                ('approval_date', models.DateTimeField(blank=True, null=True)),
                ('loan_term', models.CharField(blank=True, max_length=20, null=True)),
                ('colleteral', models.CharField(blank=True, max_length=20, null=True)),
                ('amount', models.CharField(blank=True, max_length=20, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loan_client', to='users.Clients', verbose_name='Client')),
                ('signing_officer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loan_officer', to='users.LoanOfficer', verbose_name='Account Officer')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department', to='users.Manager'),
        ),
        migrations.AddField(
            model_name='department',
            name='organization',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='department', to='users.Organization', verbose_name='Department'),
        ),
        migrations.AddField(
            model_name='clients',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Department'),
        ),
        migrations.AddField(
            model_name='clients',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Organization'),
        ),
        migrations.AddField(
            model_name='clients',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client', to='users.AccountUser', verbose_name='Client'),
        ),
        migrations.AddField(
            model_name='clients',
            name='signing_officer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_account_officer', to='users.LoanOfficer', verbose_name='Account Officer'),
        ),
        migrations.AddField(
            model_name='accountuser',
            name='user_role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Role'),
        ),
    ]
