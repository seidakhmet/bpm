# Generated by Django 4.2 on 2024-01-31 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="businessprocess",
            name="has_row_numbers",
        ),
        migrations.RemoveField(
            model_name="businessprocess",
            name="parser_type",
        ),
        migrations.RemoveField(
            model_name="task",
            name="row_index",
        ),
        migrations.AddField(
            model_name="businessprocess",
            name="dgd_code_column",
            field=models.CharField(
                choices=[
                    (0, "A column"),
                    (1, "B column"),
                    (2, "C column"),
                    (3, "D column"),
                    (4, "E column"),
                    (5, "F column"),
                    (6, "G column"),
                    (7, "H column"),
                    (8, "I column"),
                    (9, "J column"),
                    (10, "K column"),
                    (11, "L column"),
                    (12, "M column"),
                    (13, "N column"),
                    (14, "O column"),
                    (15, "P column"),
                    (16, "Q column"),
                    (17, "R column"),
                    (18, "S column"),
                    (19, "T column"),
                    (20, "U column"),
                    (21, "V column"),
                    (22, "W column"),
                    (23, "X column"),
                    (24, "Y column"),
                    (25, "Z column"),
                ],
                default=0,
                max_length=255,
                verbose_name="DGD code column",
            ),
        ),
        migrations.AddField(
            model_name="businessprocess",
            name="dgd_name_column",
            field=models.CharField(
                choices=[
                    (0, "A column"),
                    (1, "B column"),
                    (2, "C column"),
                    (3, "D column"),
                    (4, "E column"),
                    (5, "F column"),
                    (6, "G column"),
                    (7, "H column"),
                    (8, "I column"),
                    (9, "J column"),
                    (10, "K column"),
                    (11, "L column"),
                    (12, "M column"),
                    (13, "N column"),
                    (14, "O column"),
                    (15, "P column"),
                    (16, "Q column"),
                    (17, "R column"),
                    (18, "S column"),
                    (19, "T column"),
                    (20, "U column"),
                    (21, "V column"),
                    (22, "W column"),
                    (23, "X column"),
                    (24, "Y column"),
                    (25, "Z column"),
                ],
                default=1,
                max_length=255,
                verbose_name="DGD name column",
            ),
        ),
        migrations.AddField(
            model_name="businessprocess",
            name="ugd_code_column",
            field=models.CharField(
                blank=True,
                choices=[
                    (0, "A column"),
                    (1, "B column"),
                    (2, "C column"),
                    (3, "D column"),
                    (4, "E column"),
                    (5, "F column"),
                    (6, "G column"),
                    (7, "H column"),
                    (8, "I column"),
                    (9, "J column"),
                    (10, "K column"),
                    (11, "L column"),
                    (12, "M column"),
                    (13, "N column"),
                    (14, "O column"),
                    (15, "P column"),
                    (16, "Q column"),
                    (17, "R column"),
                    (18, "S column"),
                    (19, "T column"),
                    (20, "U column"),
                    (21, "V column"),
                    (22, "W column"),
                    (23, "X column"),
                    (24, "Y column"),
                    (25, "Z column"),
                ],
                default=2,
                max_length=255,
                null=True,
                verbose_name="UGD code column",
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="index",
            field=models.CharField(default=0, verbose_name="Index"),
        ),
        migrations.AlterField(
            model_name="task",
            name="business_process",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="tasks.businessprocess",
                verbose_name="Business process",
            ),
        ),
        migrations.AlterField(
            model_name="taskcolumn",
            name="column_index",
            field=models.IntegerField(default=0, verbose_name="Column index"),
        ),
    ]