# Generated by Django 4.2.5 on 2023-11-23 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicio', '0011_alter_frecuencia_dia_alter_servicio_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='frecuencia',
            name='servicio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='frecuencias', to='servicio.servicio'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='frecuencia',
            name='dia',
            field=models.PositiveIntegerField(choices=[(1, 'Lunes'), (5, 'Viernes'), (3, 'Miercoles'), (4, 'Jueves'), (6, 'Sabado'), (2, 'Martes')]),
        ),
        migrations.AlterField(
            model_name='frecuencia',
            name='turno',
            field=models.PositiveIntegerField(choices=[(1, 'Mañana'), (3, 'Noche'), (2, 'Tarde')]),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='estado',
            field=models.PositiveIntegerField(choices=[(7, 'Cancelado'), (4, 'En Curso'), (3, 'Contratado'), (2, 'Vencido'), (5, 'Suspendido'), (6, 'Finalizado'), (1, 'Presupuestodo')]),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='tipo',
            field=models.PositiveIntegerField(choices=[(2, 'Determinado'), (1, 'Eventual')]),
        ),
    ]