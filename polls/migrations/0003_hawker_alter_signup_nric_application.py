# Generated by Django 5.1.6 on 2025-02-09 04:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_signup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hawker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('hawker_id', models.PositiveIntegerField(verbose_name='Hawker ID')),
            ],
        ),
        migrations.AlterField(
            model_name='signup',
            name='nric',
            field=models.CharField(help_text='Enter a valid NRIC (unique).', max_length=15, unique=True, verbose_name='NRIC'),
        ),
        migrations.CreateModel(
            name='application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_id', models.PositiveIntegerField(blank=True, help_text='ID of the manager if applicable.', null=True, verbose_name='Manager ID')),
                ('application_date', models.DateTimeField()),
                ('application_status', models.CharField(choices=[('scheduled', 'Scheduled'), ('not_scheduled', 'Not Scheduled')], default='not_scheduled', max_length=15)),
                ('hawker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='polls.hawker')),
            ],
        ),
    ]
