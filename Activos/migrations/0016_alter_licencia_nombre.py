# Generated by Django 3.2.8 on 2024-01-17 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activos', '0015_auto_20240116_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licencia',
            name='nombre',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Nombre'),
        ),
    ]
