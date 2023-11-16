# Generated by Django 4.2.5 on 2023-11-12 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_cliente_tipopersona_alter_insumo_unidad_med_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empleado',
            name='sueldo_basico',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tipo',
            field=models.PositiveIntegerField(choices=[(1, 'Ocacional'), (2, 'Habitual')], default=1),
        ),
        migrations.AlterField(
            model_name='insumo',
            name='unidad_med',
            field=models.IntegerField(choices=[(1, 'gr'), (3, 'ml'), (4, 'Lts'), (2, 'Kg')]),
        ),
        migrations.AlterField(
            model_name='tiposervicio',
            name='unidad_medida',
            field=models.PositiveIntegerField(choices=[(1, 'm2'), (2, 'unidad')]),
        ),
    ]