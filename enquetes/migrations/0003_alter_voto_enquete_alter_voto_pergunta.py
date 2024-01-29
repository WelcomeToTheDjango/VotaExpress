# Generated by Django 5.0.1 on 2024-01-29 21:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("enquetes", "0002_alter_voto_usuario"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voto",
            name="enquete",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="votos",
                to="enquetes.enquete",
            ),
        ),
        migrations.AlterField(
            model_name="voto",
            name="pergunta",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="votos",
                to="enquetes.pergunta",
            ),
        ),
    ]
