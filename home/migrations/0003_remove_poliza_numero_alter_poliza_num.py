# Generated by Django 5.1.2 on 2024-11-12 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_poliza_nombre_poliza_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poliza',
            name='numero',
        ),
        migrations.AlterField(
            model_name='poliza',
            name='num',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
