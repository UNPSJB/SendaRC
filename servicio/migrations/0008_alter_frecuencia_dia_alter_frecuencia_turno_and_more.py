# Generated by Django 4.2.5 on 2025-07-15 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicio', '0007_alter_frecuencia_dia_alter_frecuencia_turno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frecuencia',
            name='dia',
            field=models.PositiveIntegerField(choices=[(3, 'Miercoles'), (4, 'Jueves'), (6, 'Sabado'), (5, 'Viernes'), (1, 'Lunes'), (2, 'Martes')]),
        ),
        migrations.AlterField(
            model_name='frecuencia',
            name='turno',
            field=models.PositiveIntegerField(choices=[(3, 'Noche'), (2, 'Tarde'), (1, 'Mañana')]),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='estado',
            field=models.PositiveIntegerField(choices=[(6, 'Finalizado'), (3, 'Contratado'), (7, 'Cancelado'), (2, 'Vencido'), (5, 'Suspendido'), (1, 'Presupuestado'), (4, 'En Curso')]),
        ),
    ]
