# Generated by Django 4.2.5 on 2023-11-10 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_cliente_tipo_alter_cliente_tipopersona_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='unidad_med',
            field=models.IntegerField(choices=[(4, 'Lts'), (2, 'Kg'), (1, 'gr'), (3, 'ml')]),
        ),
        migrations.AlterField(
            model_name='tiposervicio',
            name='unidad_medida',
            field=models.PositiveIntegerField(choices=[(2, 'unidad'), (1, 'm2')]),
        ),
    ]
