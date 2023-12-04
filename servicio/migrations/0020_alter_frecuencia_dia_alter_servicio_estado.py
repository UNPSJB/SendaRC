# Generated by Django 4.2.5 on 2023-12-02 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicio', '0019_alter_frecuencia_dia_alter_frecuencia_empleados_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frecuencia',
            name='dia',
            field=models.PositiveIntegerField(choices=[(6, 'Sabado'), (1, 'Lunes'), (4, 'Jueves'), (5, 'Viernes'), (3, 'Miercoles'), (2, 'Martes')]),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='estado',
            field=models.PositiveIntegerField(choices=[(3, 'Contratado'), (2, 'Vencido'), (7, 'Cancelado'), (6, 'Finalizado'), (4, 'En Curso'), (1, 'Presupuestado'), (5, 'Suspendido')]),
        ),
    ]
