# Generated by Django 3.0.8 on 2021-02-27 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210227_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='created_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
    ]
