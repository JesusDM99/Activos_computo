# Generated by Django 5.0 on 2024-03-04 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activos', '0017_alter_licencia_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licencia',
            name='nombre',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='licencia',
            name='precio_compra',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Precio Compra'),
        ),
    ]