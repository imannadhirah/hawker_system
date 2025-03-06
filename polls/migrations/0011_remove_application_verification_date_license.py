# Generated by Django 5.1.6 on 2025-02-10 05:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_alter_application_application_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='verification_date',
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_id', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('license_holder', models.CharField(blank=True, max_length=100, null=True)),
                ('nric', models.CharField(blank=True, max_length=15, null=True)),
                ('business_name', models.CharField(blank=True, max_length=100, null=True)),
                ('license_status', models.CharField(blank=True, choices=[('pending', 'PENDING'), ('active', 'ACTIVE'), ('expired', 'EXPIRED')], default='pending', max_length=10, null=True)),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_until', models.DateField(blank=True, null=True)),
                ('application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='license', to='polls.application')),
            ],
        ),
    ]
