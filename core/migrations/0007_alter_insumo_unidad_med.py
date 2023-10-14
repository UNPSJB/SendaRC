# Generated by Django 4.2.5 on 2023-10-12 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_cliente_tipo_alter_insumo_unidad_med_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='unidad_med',
            field=models.IntegerField(choices=[(3, 'ml'), (4, 'Lts'), (2, 'Kg'), (1, 'gr')]),
        ),
    ]
