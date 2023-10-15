# Generated by Django 4.2.5 on 2023-10-15 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_numdocumento_empleado_numdni_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='tipo',
            field=models.PositiveIntegerField(choices=[(1, 'Ocacional'), (2, 'Habitual')]),
        ),
        migrations.AlterField(
            model_name='insumo',
            name='unidad_med',
            field=models.IntegerField(choices=[(4, 'Lts'), (3, 'ml'), (1, 'gr'), (2, 'Kg')]),
        ),
        migrations.AlterField(
            model_name='tiposervicio',
            name='unidad_medida',
            field=models.PositiveIntegerField(choices=[(2, 'unidad'), (1, 'm2')]),
        ),
    ]
