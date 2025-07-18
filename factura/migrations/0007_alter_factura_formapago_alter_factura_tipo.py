# Generated by Django 4.2.5 on 2025-07-15 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factura', '0006_alter_factura_formapago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='formaPago',
            field=models.PositiveIntegerField(choices=[(1, 'Efectivo'), (3, 'Transferencia'), (2, 'Cheque')], null=True),
        ),
        migrations.AlterField(
            model_name='factura',
            name='tipo',
            field=models.PositiveIntegerField(choices=[(1, 'Seña'), (2, 'Unica'), (3, 'Mensual')]),
        ),
    ]
