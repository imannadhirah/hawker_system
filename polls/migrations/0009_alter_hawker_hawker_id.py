# Generated by Django 5.1.6 on 2025-02-10 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_remove_application_application_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hawker',
            name='hawker_id',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='NRIC'),
        ),
    ]
