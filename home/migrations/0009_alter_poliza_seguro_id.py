# Generated by Django 5.1.2 on 2024-11-12 02:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_remove_poliza_tipo_seguro_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poliza',
            name='seguro_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.seguro'),
        ),
    ]
