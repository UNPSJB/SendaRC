# Generated by Django 4.2.5 on 2023-11-29 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_rename_estado_insumo_activo_alter_cliente_tipo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='tipo',
            field=models.PositiveIntegerField(choices=[(1, 'Ocacional'), (2, 'Habitual')], default=1),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tipoPersona',
            field=models.PositiveIntegerField(choices=[(2, 'Juridico'), (1, 'Particular')]),
        ),
        migrations.AlterField(
            model_name='tiposervicio',
            name='unidad_medida',
            field=models.PositiveIntegerField(choices=[(2, 'unidad'), (1, 'm2')]),
        ),
    ]
