# Generated by Django 3.2.8 on 2024-01-12 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activos', '0002_auto_20240111_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activo',
            name='tic',
            field=models.CharField(max_length=30, null=True, verbose_name='TIC'),
        ),
    ]
