# Generated by Django 5.1.6 on 2025-02-09 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_hawker_alter_signup_nric_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='application_id',
            field=models.PositiveIntegerField(blank=True, help_text='ID of the manager if applicable.', null=True, verbose_name='Application ID'),
        ),
    ]
