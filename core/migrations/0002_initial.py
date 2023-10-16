# Generated by Django 4.2.5 on 2023-10-15 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CantInsumoServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('numdocumento', models.IntegerField(primary_key=True, serialize=False)),
                ('numlegajo', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('telefono', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('sueldo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Insumo',
            fields=[
                ('codigo', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=50)),
                ('unidad_med', models.IntegerField(choices=[(3, 'ml'), (2, 'Kg'), (4, 'Lts'), (1, 'gr')])),
                ('contenido_neto', models.IntegerField()),
                ('marca', models.CharField(max_length=50)),
                ('cantidad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('cp', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Maquinaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('marca', models.CharField(max_length=50)),
                ('cantidad', models.IntegerField()),
                ('observaciones', models.TextField()),
                ('baja', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='TipoServicio',
            fields=[
                ('codigo', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=50)),
                ('unidad_medida', models.PositiveIntegerField(choices=[(1, 'm2'), (2, 'unidad')])),
                ('precio', models.IntegerField()),
                ('insumos', models.ManyToManyField(through='core.CantInsumoServicio', to='core.insumo')),
                ('maquinarias', models.ManyToManyField(to='core.maquinaria')),
            ],
        ),
        migrations.CreateModel(
            name='Sancion',
            fields=[
                ('tipo', models.PositiveIntegerField(choices=[(1, 'Correcion'), (2, 'Suspension')])),
                ('nroSancion', models.IntegerField(primary_key=True, serialize=False)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.empleado')),
            ],
        ),
        migrations.AddField(
            model_name='empleado',
            name='localidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.localidad'),
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=50)),
                ('tipo', models.PositiveIntegerField(choices=[(1, 'Ocacional'), (2, 'Habitual')])),
                ('tipoPersona', models.PositiveIntegerField(choices=[(1, 'Particular'), (2, 'Juridico')])),
                ('cuil', models.IntegerField(primary_key=True, serialize=False)),
                ('telefono', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('localidad', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.localidad')),
            ],
        ),
        migrations.AddField(
            model_name='cantinsumoservicio',
            name='insumo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.insumo'),
        ),
        migrations.AddField(
            model_name='cantinsumoservicio',
            name='tipoServicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.tiposervicio'),
        ),
    ]
