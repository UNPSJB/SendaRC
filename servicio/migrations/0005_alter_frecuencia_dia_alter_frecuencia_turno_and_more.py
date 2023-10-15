# Generated by Django 4.2.5 on 2023-10-15 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicio', '0004_alter_servicio_estado_alter_servicio_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frecuencia',
            name='dia',
            field=models.PositiveIntegerField(choices=[(6, 'Sabado'), (2, 'Martes'), (1, 'Lunes'), (4, 'Jueves'), (3, 'Miercoles'), (5, 'Viernes')]),
        ),
        migrations.AlterField(
            model_name='frecuencia',
            name='turno',
            field=models.PositiveIntegerField(choices=[(1, 'Mañana'), (2, 'Tarde'), (3, 'Noche')]),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='estado',
            field=models.PositiveIntegerField(choices=[(5, 'Suspendido'), (4, 'En Curso'), (6, 'Finalizado'), (3, 'Contratado'), (1, 'Presupuestodo'), (7, 'Cancelado'), (2, 'Vencido')]),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='tipo',
            field=models.PositiveIntegerField(choices=[(1, 'Eventual'), (2, 'Determinado')]),
        ),
    ]
