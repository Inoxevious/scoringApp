# Generated by Django 3.0.8 on 2021-02-27 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='bp_number',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='business_category',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='entity_type',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='registration_number',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
    ]