# Generated by Django 4.2.5 on 2025-07-26 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CantServicioTipoServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_emision', models.DateField(auto_now=True)),
                ('plazo_vigencia', models.DateField()),
                ('direccion', models.CharField(max_length=90)),
                ('metros2', models.IntegerField()),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('porcentaje', models.IntegerField()),
                ('cant_empleados', models.IntegerField()),
                ('importe_total', models.IntegerField()),
                ('estado', models.PositiveIntegerField(choices=[(4, 'En Curso'), (6, 'Finalizado'), (7, 'Cancelado'), (3, 'Contratado'), (2, 'Vencido'), (1, 'Presupuestado'), (5, 'Suspendido')])),
                ('tipo', models.PositiveIntegerField(choices=[(2, 'Determinado'), (1, 'Eventual')])),
                ('fecha_inicio', models.DateField(null=True)),
                ('fecha_finaliza', models.DateField(null=True)),
                ('fecha_cancelada', models.DateField(null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.cliente')),
                ('empleado', models.ManyToManyField(null=True, to='core.empleado')),
                ('localidad', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.localidad')),
                ('tipoServicios', models.ManyToManyField(through='servicio.CantServicioTipoServicio', to='core.tiposervicio')),
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
            name='Frecuencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.PositiveIntegerField(choices=[(1, 'Lunes'), (6, 'Sabado'), (4, 'Jueves'), (3, 'Miercoles'), (5, 'Viernes'), (2, 'Martes')])),
                ('turno', models.PositiveIntegerField(choices=[(2, 'Tarde'), (3, 'Noche'), (1, 'Mañana')])),
                ('empleados', models.ManyToManyField(null=True, related_name='frecuencias', to='core.empleado')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frecuencias', to='servicio.servicio')),
            ],
        ),
        migrations.AddField(
            model_name='cantserviciotiposervicio',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='servicio.servicio'),
        ),
        migrations.AddField(
            model_name='cantserviciotiposervicio',
            name='tipoServicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.tiposervicio'),
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora_entrada', models.TimeField()),
                ('hora_salida', models.TimeField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.empleado')),
                ('frecuencia', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='servicio.frecuencia')),
            ],
        ),
    ]
