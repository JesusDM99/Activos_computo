# Generated by Django 3.2.8 on 2024-01-12 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activos', '0006_auto_20240111_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='nit',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nit'),
        ),
        migrations.AlterField(
            model_name='activo',
            name='licencia',
            field=models.ManyToManyField(blank=True, null=True, related_name='activos_licencia', to='Activos.Licencia'),
        ),
    ]
