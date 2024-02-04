# Generated by Django 4.2 on 2024-01-31 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tasks", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="taskcellvaluelog",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="created_task_cell_values",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created by",
            ),
        ),
        migrations.AddField(
            model_name="taskcellvaluelog",
            name="task_cell",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="logs",
                to="tasks.taskcell",
                verbose_name="Task cell",
            ),
        ),
        migrations.AddField(
            model_name="taskcell",
            name="business_process",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cells",
                to="tasks.businessprocess",
                verbose_name="Business process",
            ),
        ),
        migrations.AddField(
            model_name="taskcell",
            name="column",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cells",
                to="tasks.taskcolumn",
                verbose_name="Task column",
            ),
        ),
        migrations.AddField(
            model_name="taskcell",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="cells", to="tasks.task", verbose_name="Task"
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="business_process",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rows",
                to="tasks.businessprocess",
                verbose_name="Business process",
            ),
        ),
        migrations.AddField(
            model_name="businessprocess",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="created_business_processes",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created by",
            ),
        ),
    ]
