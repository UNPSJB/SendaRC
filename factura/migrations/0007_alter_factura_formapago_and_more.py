# Generated by Django 4.2.5 on 2023-12-03 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factura', '0006_factura_tipo_alter_factura_formapago_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='formaPago',
            field=models.PositiveIntegerField(choices=[(2, 'Cheque'), (3, 'Transferencia'), (1, 'Efectivo')], null=True),
        ),
        migrations.AlterField(
            model_name='factura',
            name='periodoServicio',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='factura',
            name='tipo',
            field=models.PositiveIntegerField(choices=[(1, 'Seña'), (2, 'Unica'), (3, 'Mensual')]),
        ),
    ]
