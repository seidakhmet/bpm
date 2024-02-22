# Generated by Django 4.2 on 2024-02-19 04:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0018_alter_businessprocess_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="taskcell",
            name="column_index",
            field=models.IntegerField(default=0, verbose_name="Column index"),
        ),
        migrations.AddField(
            model_name="taskcell",
            name="column_type",
            field=models.CharField(
                choices=[
                    ("string", "String"),
                    ("text", "Text"),
                    ("integer", "Integer"),
                    ("float", "Float"),
                    ("date", "Date"),
                    ("date_time", "Date and time"),
                    ("boolean", "Boolean"),
                ],
                default="string",
                max_length=50,
                verbose_name="Column type",
            ),
        ),
        migrations.AddField(
            model_name="taskcell",
            name="is_editable",
            field=models.BooleanField(default=True, verbose_name="Is editable"),
        ),
    ]
