# Generated by Django 5.1.6 on 2025-02-10 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_inspector_remove_application_inspection_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inspection',
            old_name='inspection',
            new_name='application',
        ),
    ]
