# Generated by Django 5.1.7 on 2025-05-15 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_recordcollection_exam_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recordsubmission',
            old_name='course_name',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='recordsubmission',
            old_name='inv_dept',
            new_name='department',
        ),
    ]
