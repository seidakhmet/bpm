# Generated by Django 4.2 on 2024-02-14 13:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0017_remove_taskdelegation_delegated_to_group_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="businessprocess",
            name="status",
            field=models.CharField(
                choices=[
                    ("created", "Created"),
                    ("published", "Published"),
                    ("completed", "Completed"),
                    ("canceled", "Canceled"),
                ],
                default="created",
                max_length=100,
                verbose_name="Status",
            ),
        ),
        migrations.AlterField(
            model_name="taskdelegation",
            name="status",
            field=models.CharField(
                choices=[
                    ("delegated_to_user", "Delegated to user"),
                    ("delegated_to_group", "Delegated to group"),
                    ("self_delegated", "Self-delegated"),
                    ("returned_to_delegator", "Returned to delegator"),
                    ("sent_to_approval", "Sent to approval"),
                    ("sent_to_rework", "Sent to rework"),
                ],
                default="delegated_to_user",
                max_length=100,
                verbose_name="Status",
            ),
        ),
    ]
