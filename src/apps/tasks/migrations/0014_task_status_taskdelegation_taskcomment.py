# Generated by Django 4.2 on 2024-02-06 03:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tasks", "0013_alter_taskstatus_required_task_columns"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="status",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tasks",
                to="tasks.taskstatus",
                verbose_name="Status",
            ),
        ),
        migrations.CreateModel(
            name="TaskDelegation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created time")),
                ("changed_at", models.DateTimeField(auto_now=True, db_index=True, verbose_name="Last change time")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("created", "Created"),
                            ("in_progress", "In progress"),
                            ("finished", "Finished"),
                            ("accepted", "Accepted"),
                            ("rejected", "Rejected"),
                        ],
                        default="created",
                        max_length=100,
                        verbose_name="Status",
                    ),
                ),
                (
                    "delegated_to_group",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("BPM_KGD", "БПМ КГД"),
                            ("BPM_DGD_RUK_ZAM", "БПМ ДГД Руководитель заместитель"),
                            ("BPM_DGD_RUK_UPR", "БПМ ДГД Руководитель управления"),
                            ("BPM_DGD_NACH_OTD", "БПМ ДГД Начальник отдела"),
                            ("BPM_DGD_ISP", "БПМ ДГД Исполнитель"),
                            ("BPM_UGD_RUK_ZAM", "БПМ УГД Руководитель заместитель"),
                            ("BPM_UGD_RUK_OTD", "БПМ УГД Руководитель отдела"),
                            ("BPM_UGD_ISP", "БПМ УГД Исполнитель"),
                        ],
                        max_length=255,
                        null=True,
                        verbose_name="Delegated to group",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_task_delegations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "delegated_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="delegated_task_delegations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Delegated to",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="delegations",
                        to="tasks.task",
                        verbose_name="Task",
                    ),
                ),
            ],
            options={
                "verbose_name": "Task delegation",
                "verbose_name_plural": "Task delegations",
            },
        ),
        migrations.CreateModel(
            name="TaskComment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created time")),
                ("changed_at", models.DateTimeField(auto_now=True, db_index=True, verbose_name="Last change time")),
                ("text", models.TextField(verbose_name="Text")),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_task_comments",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="tasks.task",
                        verbose_name="Task",
                    ),
                ),
            ],
            options={
                "verbose_name": "Task comment",
                "verbose_name_plural": "Task comments",
            },
        ),
    ]