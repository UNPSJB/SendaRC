# Generated by Django 4.2.5 on 2025-04-21 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_cliente_tipo_alter_cliente_tipopersona_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='unidad_med',
            field=models.IntegerField(choices=[(2, 'Kg'), (4, 'Lts'), (1, 'gr'), (3, 'ml')]),
        ),
        migrations.AlterField(
            model_name='sancion',
            name='tipo',
            field=models.PositiveIntegerField(choices=[(2, 'Suspension'), (1, 'Correcion')]),
        ),
    ]
