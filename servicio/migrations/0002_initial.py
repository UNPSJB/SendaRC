# Generated by Django 4.2.5 on 2023-10-19 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_initial'),
        ('servicio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_emision', models.DateField(auto_now=True)),
                ('plazo_vigencia', models.DateField()),
                ('direccion', models.CharField(max_length=90)),
                ('metros2', models.IntegerField()),
                ('observaciones', models.TextField()),
                ('porcentaje', models.IntegerField()),
                ('cant_empleados', models.IntegerField()),
                ('importe_total', models.IntegerField()),
                ('estado', models.PositiveIntegerField(choices=[(7, 'Cancelado'), (6, 'Finalizado'), (2, 'Vencido'), (1, 'Presupuestodo'), (5, 'Suspendido'), (4, 'En Curso'), (3, 'Contratado')])),
                ('tipo', models.PositiveIntegerField(choices=[(1, 'Eventual'), (2, 'Determinado')])),
                ('fecha_inicio', models.DateField()),
                ('fecha_finaliza', models.DateField()),
                ('fecha_cancelada', models.DateField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.cliente')),
                ('empleado', models.ManyToManyField(to='core.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Reclamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=400)),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='servicio.servicio')),
            ],
        ),
        migrations.CreateModel(
            name='HojaTrabajo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.empleado')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='servicio.servicio')),
            ],
        ),
        migrations.CreateModel(
            name='Frecuencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.PositiveIntegerField(choices=[(5, 'Viernes'), (3, 'Miercoles'), (2, 'Martes'), (1, 'Lunes'), (6, 'Sabado'), (4, 'Jueves')])),
                ('turno', models.PositiveIntegerField(choices=[(3, 'Noche'), (1, 'Mañana'), (2, 'Tarde')])),
                ('horaInicio', models.DateTimeField()),
                ('horaFin', models.DateTimeField()),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='servicio.servicio')),
            ],
        ),
    ]
