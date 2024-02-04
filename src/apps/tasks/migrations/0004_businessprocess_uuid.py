# Generated by Django 4.2 on 2024-01-31 11:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0003_remove_businessprocess_has_row_numbers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="businessprocess",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="UUID identification"),
        ),
    ]