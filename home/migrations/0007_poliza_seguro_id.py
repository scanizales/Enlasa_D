# Generated by Django 5.1.2 on 2024-11-12 02:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_cliente_celular_alter_cliente_telefono'),
    ]

    operations = [
        migrations.AddField(
            model_name='poliza',
            name='seguro_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.seguro'),
        ),
    ]