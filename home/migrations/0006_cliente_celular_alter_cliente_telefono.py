# Generated by Django 5.1.2 on 2024-11-12 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_usuario_managers_usuario_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='celular',
            field=models.CharField(default=1, max_length=50),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(max_length=50, null=True),
        ),
    ]