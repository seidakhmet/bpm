# Generated by Django 4.2 on 2024-02-04 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0009_remove_businessprocess_deadline"),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskStatus",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created time")),
                ("changed_at", models.DateTimeField(auto_now=True, db_index=True, verbose_name="Last change time")),
                ("status_name", models.CharField(max_length=255, verbose_name="Status name")),
                (
                    "required_task_columns",
                    models.ManyToManyField(
                        related_name="required_statuses", to="tasks.taskcolumn", verbose_name="Required task columns"
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="statuses",
                        to="tasks.task",
                        verbose_name="Task",
                    ),
                ),
            ],
            options={
                "verbose_name": "Task status",
                "verbose_name_plural": "Task statuses",
            },
        ),
    ]
