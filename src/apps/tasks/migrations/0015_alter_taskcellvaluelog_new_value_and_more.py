# Generated by Django 4.2 on 2024-02-08 12:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0014_task_status_taskdelegation_taskcomment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskcellvaluelog",
            name="new_value",
            field=models.TextField(blank=True, null=True, verbose_name="New value"),
        ),
        migrations.AlterField(
            model_name="taskcellvaluelog",
            name="old_value",
            field=models.TextField(blank=True, null=True, verbose_name="Old value"),
        ),
    ]
