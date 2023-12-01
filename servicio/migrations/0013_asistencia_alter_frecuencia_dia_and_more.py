# Generated by Django 4.2.5 on 2023-11-24 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_insumo_unidad_med_alter_sancion_tipo_and_more'),
        ('servicio', '0012_frecuencia_servicio_alter_frecuencia_dia_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora_entrada', models.TimeField()),
                ('hora_salida', models.TimeField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.empleado')),
            ],
        ),
        migrations.AlterField(
            model_name='frecuencia',
            name='dia',
            field=models.PositiveIntegerField(choices=[(3, 'Miercoles'), (5, 'Viernes'), (2, 'Martes'), (1, 'Lunes'), (6, 'Sabado'), (4, 'Jueves')]),
        ),
        migrations.AlterField(
            model_name='frecuencia',
            name='turno',
            field=models.PositiveIntegerField(choices=[(3, 'Noche'), (2, 'Tarde'), (1, 'Mañana')]),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='estado',
            field=models.PositiveIntegerField(choices=[(2, 'Vencido'), (4, 'En Curso'), (3, 'Contratado'), (6, 'Finalizado'), (5, 'Suspendido'), (1, 'Presupuestodo'), (7, 'Cancelado')]),
        ),
        migrations.DeleteModel(
            name='HojaTrabajo',
        ),
        migrations.AddField(
            model_name='asistencia',
            name='frecuencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='servicio.frecuencia'),
        ),
    ]