# Generated by Django 4.2.5 on 2023-10-15 03:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('nro_servicio', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_emision', models.DateField(auto_now=True)),
                ('plazo_vigencia', models.DateField()),
                ('direccion', models.CharField(max_length=90)),
                ('metros2', models.IntegerField()),
                ('observaciones', models.TextField()),
                ('porcentaje', models.IntegerField()),
                ('cant_empleados', models.IntegerField()),
                ('importe_total', models.IntegerField()),
                ('estado', models.PositiveIntegerField(choices=[(4, 'En Curso'), (6, 'Finalizado'), (7, 'Cancelado'), (2, 'Vencido'), (3, 'Contratado'), (5, 'Suspendido'), (1, 'Presupuestodo')])),
                ('tipo', models.PositiveIntegerField(choices=[(2, 'Determinado'), (1, 'Eventual')])),
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
                ('nroReclamo', models.IntegerField(primary_key=True, serialize=False)),
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
                ('dia', models.PositiveIntegerField(choices=[(4, 'Jueves'), (1, 'Lunes'), (6, 'Sabado'), (3, 'Miercoles'), (2, 'Martes'), (5, 'Viernes')])),
                ('turno', models.PositiveIntegerField(choices=[(2, 'Tarde'), (1, 'Mañana'), (3, 'Noche')])),
                ('horaInicio', models.DateTimeField()),
                ('horaFin', models.DateTimeField()),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='servicio.servicio')),
            ],
        ),
    ]
