# Generated by Django 4.2.5 on 2023-12-01 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factura', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='formaPago',
            field=models.PositiveIntegerField(choices=[(2, 'Cheque'), (3, 'Transferencia'), (1, 'Efectivo')]),
        ),
    ]