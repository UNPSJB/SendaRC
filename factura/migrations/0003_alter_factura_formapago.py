# Generated by Django 4.2.5 on 2023-12-01 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factura', '0002_alter_factura_formapago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='formaPago',
            field=models.PositiveIntegerField(choices=[(3, 'Transferencia'), (2, 'Cheque'), (1, 'Efectivo')]),
        ),
    ]