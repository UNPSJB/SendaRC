# Generated by Django 4.2.5 on 2023-11-28 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicio', '0015_alter_frecuencia_dia_alter_frecuencia_turno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frecuencia',
            name='dia',
            field=models.PositiveIntegerField(choices=[(1, 'Lunes'), (5, 'Viernes'), (4, 'Jueves'), (2, 'Martes'), (6, 'Sabado'), (3, 'Miercoles')]),
        ),
        migrations.AlterField(
            model_name='frecuencia',
            name='turno',
            field=models.PositiveIntegerField(choices=[(1, 'Mañana'), (3, 'Noche'), (2, 'Tarde')]),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='estado',
            field=models.PositiveIntegerField(choices=[(5, 'Suspendido'), (7, 'Cancelado'), (2, 'Vencido'), (4, 'En Curso'), (3, 'Contratado'), (1, 'Presupuestodo'), (6, 'Finalizado')]),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='tipo',
            field=models.PositiveIntegerField(choices=[(1, 'Eventual'), (2, 'Determinado')]),
        ),
    ]
