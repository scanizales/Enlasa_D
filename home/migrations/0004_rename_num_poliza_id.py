# Generated by Django 5.1.2 on 2024-11-12 01:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_poliza_numero_alter_poliza_num'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poliza',
            old_name='num',
            new_name='id',
        ),
    ]