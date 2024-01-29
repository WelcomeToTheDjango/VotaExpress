# Generated by Django 5.0.1 on 2024-01-29 21:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("enquetes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voto",
            name="usuario",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="votos",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
