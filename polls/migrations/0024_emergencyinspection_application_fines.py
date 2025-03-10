# Generated by Django 5.1.6 on 2025-02-11 09:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0023_alter_application_application_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='emergencyinspection',
            name='application',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emergencyins', to='polls.application'),
        ),
        migrations.CreateModel(
            name='Fines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fines_name', models.CharField(blank=True, max_length=50, null=True)),
                ('issued_date', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('fine_amount', models.CharField(blank=True, max_length=50, null=True)),
                ('fine_payment_status', models.CharField(blank=True, choices=[('unpaid', 'UNPAID'), ('paid', 'PAID')], default='unpaid', max_length=10, null=True)),
                ('application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fines', to='polls.application')),
                ('hawker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fines', to='polls.hawker')),
            ],
        ),
    ]
