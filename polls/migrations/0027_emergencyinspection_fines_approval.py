# Generated by Django 5.1.6 on 2025-02-11 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0026_remove_emergencyinspection_inspector_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='emergencyinspection',
            name='fines_approval',
            field=models.CharField(choices=[('Pass', 'Pass'), ('Approve Fines', 'Approve_Fines'), ('processing', 'processing')], default='processing', max_length=20),
        ),
    ]
