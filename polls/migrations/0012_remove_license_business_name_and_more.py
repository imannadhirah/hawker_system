# Generated by Django 5.1.6 on 2025-02-10 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_remove_application_verification_date_license'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='license',
            name='business_name',
        ),
        migrations.RemoveField(
            model_name='license',
            name='license_holder',
        ),
        migrations.RemoveField(
            model_name='license',
            name='nric',
        ),
    ]
