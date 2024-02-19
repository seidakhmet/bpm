# Generated by Django 4.2 on 2024-02-11 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
        ("tasks", "0015_alter_taskcellvaluelog_new_value_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskdelegation",
            name="delegated_to_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="delegated_task_delegations",
                to="users.bpmgroup",
                verbose_name="Delegated to group",
            ),
        ),
    ]
