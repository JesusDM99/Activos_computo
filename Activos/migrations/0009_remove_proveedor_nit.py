# Generated by Django 3.2.8 on 2024-01-13 01:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activos', '0008_alter_activo_licencia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proveedor',
            name='nit',
        ),
    ]
