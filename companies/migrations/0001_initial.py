# Generated by Django 3.0.8 on 2021-02-27 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='zim', max_length=200)),
                ('official_language', models.TextField(blank=True, null=True)),
                ('flag', models.ImageField(blank=True, null=True, upload_to='static/images/countries/flags')),
                ('longi', models.TextField(blank=True, null=True)),
                ('lat', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IncomeData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LOAN_ID', models.IntegerField(blank=True, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('workclass', models.CharField(blank=True, max_length=255, null=True)),
                ('fnlwgt', models.IntegerField(blank=True, null=True)),
                ('education', models.CharField(blank=True, max_length=255, null=True)),
                ('education_num', models.IntegerField(blank=True, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=255, null=True)),
                ('occupation', models.CharField(blank=True, max_length=255, null=True)),
                ('relationship', models.CharField(blank=True, max_length=255, null=True)),
                ('race', models.CharField(blank=True, max_length=255, null=True)),
                ('sex', models.CharField(blank=True, max_length=255, null=True)),
                ('capital_gain', models.IntegerField(blank=True, null=True)),
                ('capital_loss', models.IntegerField(blank=True, null=True)),
                ('hours_per_week', models.IntegerField(blank=True, null=True)),
                ('native_country', models.CharField(blank=True, max_length=255, null=True)),
                ('income', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Loan_History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LOAN_ID', models.IntegerField(blank=True, null=True)),
                ('NAME_CONTRACT_TYPE', models.CharField(blank=True, max_length=70, null=True)),
                ('CODE_GENDER', models.CharField(blank=True, max_length=70, null=True)),
                ('FLAG_OWN_CAR', models.CharField(blank=True, max_length=70, null=True)),
                ('FLAG_OWN_REALTY', models.CharField(blank=True, max_length=70, null=True)),
                ('NAME_TYPE_SUITE', models.CharField(blank=True, max_length=70, null=True)),
                ('NAME_INCOME_TYPE', models.CharField(blank=True, max_length=70, null=True)),
                ('NAME_EDUCATION_TYPE', models.CharField(blank=True, max_length=70, null=True)),
                ('NAME_FAMILY_STATUS', models.CharField(blank=True, max_length=70, null=True)),
                ('NAME_HOUSING_TYPE', models.CharField(blank=True, max_length=70, null=True)),
                ('OCCUPATION_TYPE', models.CharField(blank=True, max_length=70, null=True)),
                ('WEEKDAY_APPR_PROCESS_START', models.CharField(blank=True, max_length=70, null=True)),
                ('ORGANIZATION_TYPE', models.CharField(blank=True, max_length=70, null=True)),
                ('FONDKAPREMONT_MODE', models.CharField(blank=True, max_length=70, null=True)),
                ('HOUSETYPE_MODE', models.CharField(blank=True, max_length=70, null=True)),
                ('WALLSMATERIAL_MODE', models.CharField(blank=True, max_length=70, null=True)),
                ('EMERGENCYSTATE_MODE', models.CharField(blank=True, max_length=70, null=True)),
                ('TARGET', models.IntegerField(blank=True, null=True)),
                ('CNT_CHILDREN', models.IntegerField(blank=True, null=True)),
                ('AMT_INCOME_TOTAL', models.FloatField(blank=True, null=True)),
                ('AMT_CREDIT', models.FloatField(blank=True, null=True)),
                ('AMT_ANNUITY', models.FloatField(blank=True, null=True)),
                ('AMT_GOODS_PRICE', models.FloatField(blank=True, null=True)),
                ('REGION_POPULATION_RELATIVE', models.FloatField(blank=True, null=True)),
                ('DAYS_BIRTH', models.IntegerField(blank=True, null=True)),
                ('DAYS_EMPLOYED', models.IntegerField(blank=True, null=True)),
                ('DAYS_REGISTRATION', models.IntegerField(blank=True, null=True)),
                ('DAYS_ID_PUBLISH', models.IntegerField(blank=True, null=True)),
                ('OWN_CAR_AGE', models.FloatField(blank=True, null=True)),
                ('FLAG_MOBIL', models.IntegerField(blank=True, null=True)),
                ('FLAG_EMP_PHONE', models.IntegerField(blank=True, null=True)),
                ('FLAG_WORK_PHONE', models.IntegerField(blank=True, null=True)),
                ('FLAG_CONT_MOBILE', models.IntegerField(blank=True, null=True)),
                ('FLAG_PHONE', models.IntegerField(blank=True, null=True)),
                ('FLAG_EMAIL', models.IntegerField(blank=True, null=True)),
                ('CNT_FAM_MEMBERS', models.IntegerField(blank=True, null=True)),
                ('REGION_RATING_CLIENT', models.IntegerField(blank=True, null=True)),
                ('REGION_RATING_CLIENT_W_CITY', models.IntegerField(blank=True, null=True)),
                ('HOUR_APPR_PROCESS_START', models.IntegerField(blank=True, null=True)),
                ('REG_REGION_NOT_LIVE_REGION', models.IntegerField(blank=True, null=True)),
                ('REG_REGION_NOT_WORK_REGION', models.IntegerField(blank=True, null=True)),
                ('LIVE_REGION_NOT_WORK_REGION', models.IntegerField(blank=True, null=True)),
                ('REG_CITY_NOT_LIVE_CITY', models.IntegerField(blank=True, null=True)),
                ('REG_CITY_NOT_WORK_CITY', models.IntegerField(blank=True, null=True)),
                ('LIVE_CITY_NOT_WORK_CITY', models.IntegerField(blank=True, null=True)),
                ('EXT_SOURCE_1', models.FloatField(blank=True, null=True)),
                ('EXT_SOURCE_2', models.FloatField(blank=True, null=True)),
                ('EXT_SOURCE_3', models.FloatField(blank=True, null=True)),
                ('APARTMENTS_AVG', models.FloatField(blank=True, null=True)),
                ('BASEMENTAREA_AVG', models.FloatField(blank=True, null=True)),
                ('YEARS_BEGINEXPLUATATION_AVG', models.FloatField(blank=True, null=True)),
                ('YEARS_BUILD_AVG', models.FloatField(blank=True, null=True)),
                ('COMMONAREA_AVG', models.FloatField(blank=True, null=True)),
                ('ELEVATORS_AVG', models.FloatField(blank=True, null=True)),
                ('ENTRANCES_AVG', models.FloatField(blank=True, null=True)),
                ('FLOORSMAX_AVG', models.FloatField(blank=True, null=True)),
                ('FLOORSMIN_AVG', models.FloatField(blank=True, null=True)),
                ('LANDAREA_AVG', models.FloatField(blank=True, null=True)),
                ('LIVINGAPARTMENTS_AVG', models.FloatField(blank=True, null=True)),
                ('LIVINGAREA_AVG', models.FloatField(blank=True, null=True)),
                ('NONLIVINGAPARTMENTS_AVG', models.FloatField(blank=True, null=True)),
                ('NONLIVINGAREA_AVG', models.FloatField(blank=True, null=True)),
                ('APARTMENTS_MODE', models.FloatField(blank=True, null=True)),
                ('BASEMENTAREA_MODE', models.FloatField(blank=True, null=True)),
                ('YEARS_BEGINEXPLUATATION_MODE', models.FloatField(blank=True, null=True)),
                ('YEARS_BUILD_MODE', models.FloatField(blank=True, null=True)),
                ('COMMONAREA_MODE', models.FloatField(blank=True, null=True)),
                ('ELEVATORS_MODE', models.FloatField(blank=True, null=True)),
                ('ENTRANCES_MODE', models.FloatField(blank=True, null=True)),
                ('FLOORSMAX_MODE', models.FloatField(blank=True, null=True)),
                ('FLOORSMIN_MODE', models.FloatField(blank=True, null=True)),
                ('LANDAREA_MODE', models.FloatField(blank=True, null=True)),
                ('LIVINGAPARTMENTS_MODE', models.FloatField(blank=True, null=True)),
                ('LIVINGAREA_MODE', models.FloatField(blank=True, null=True)),
                ('NONLIVINGAPARTMENTS_MODE', models.FloatField(blank=True, null=True)),
                ('NONLIVINGAREA_MODE', models.FloatField(blank=True, null=True)),
                ('APARTMENTS_MEDI', models.FloatField(blank=True, null=True)),
                ('BASEMENTAREA_MEDI', models.FloatField(blank=True, null=True)),
                ('YEARS_BEGINEXPLUATATION_MEDI', models.FloatField(blank=True, null=True)),
                ('YEARS_BUILD_MEDI', models.FloatField(blank=True, null=True)),
                ('COMMONAREA_MEDI', models.FloatField(blank=True, null=True)),
                ('ELEVATORS_MEDI', models.FloatField(blank=True, null=True)),
                ('ENTRANCES_MEDI', models.FloatField(blank=True, null=True)),
                ('FLOORSMAX_MEDI', models.FloatField(blank=True, null=True)),
                ('FLOORSMIN_MEDI', models.FloatField(blank=True, null=True)),
                ('LANDAREA_MEDI', models.FloatField(blank=True, null=True)),
                ('LIVINGAPARTMENTS_MEDI', models.FloatField(blank=True, null=True)),
                ('LIVINGAREA_MEDI', models.FloatField(blank=True, null=True)),
                ('NONLIVINGAPARTMENTS_MEDI', models.FloatField(blank=True, null=True)),
                ('NONLIVINGAREA_MEDI', models.FloatField(blank=True, null=True)),
                ('TOTALAREA_MODE', models.FloatField(blank=True, null=True)),
                ('OBS_30_CNT_SOCIAL_CIRCLE', models.FloatField(blank=True, null=True)),
                ('DEF_30_CNT_SOCIAL_CIRCLE', models.FloatField(blank=True, null=True)),
                ('OBS_60_CNT_SOCIAL_CIRCLE', models.FloatField(blank=True, null=True)),
                ('DEF_60_CNT_SOCIAL_CIRCLE', models.FloatField(blank=True, null=True)),
                ('DAYS_LAST_PHONE_CHANGE', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_2', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_3', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_4', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_5', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_6', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_7', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_8', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_9', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_10', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_11', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_12', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_13', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_14', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_15', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_16', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_17', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_18', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_19', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_20', models.IntegerField(blank=True, null=True)),
                ('FLAG_DOCUMENT_21', models.IntegerField(blank=True, null=True)),
                ('AMT_REQ_CREDIT_BUREAU_HOUR', models.FloatField(blank=True, null=True)),
                ('AMT_REQ_CREDIT_BUREAU_DAY', models.FloatField(blank=True, null=True)),
                ('AMT_REQ_CREDIT_BUREAU_WEEK', models.FloatField(blank=True, null=True)),
                ('AMT_REQ_CREDIT_BUREAU_MON', models.FloatField(blank=True, null=True)),
                ('AMT_REQ_CREDIT_BUREAU_QRT', models.FloatField(blank=True, null=True)),
                ('AMT_REQ_CREDIT_BUREAU_YEAR', models.FloatField(blank=True, null=True)),
                ('OFFICER_ID', models.CharField(blank=True, max_length=70, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LoanApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LOAN_ID', models.IntegerField(blank=True, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('ed', models.IntegerField(blank=True, null=True)),
                ('employ', models.IntegerField(blank=True, null=True)),
                ('address', models.IntegerField(blank=True, null=True)),
                ('income', models.IntegerField(blank=True, null=True)),
                ('debtinc', models.FloatField(blank=True, null=True)),
                ('creddebt', models.FloatField(blank=True, null=True)),
                ('othdebt', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
