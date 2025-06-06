# Generated by Django 5.1.7 on 2025-04-01 15:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divisions', '0002_alter_employee_options_remove_employee_content_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={},
        ),
        migrations.RemoveField(
            model_name='department',
            name='leader',
        ),
        migrations.RemoveField(
            model_name='division',
            name='leader',
        ),
        migrations.RemoveField(
            model_name='service',
            name='leader',
        ),
        migrations.RemoveField(
            model_name='team',
            name='members',
        ),
        migrations.AddField(
            model_name='employee',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='divisions.team', verbose_name='Группа'),
        ),
    ]
