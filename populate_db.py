import os
import django
import random
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SendaRC.settings')  # Replace 'your_project' with your project name
django.setup()

from core.models import Localidad, Cliente, Empleado, Insumo, Maquinaria, TipoServicio, CantInsumoServicio

def populate_data():
    # Localidad data (Argentine localities with postal codes)
    localidades_data = [
        {'cp': 'C1001', 'nombre': 'Buenos Aires'},
        {'cp': 'X5000', 'nombre': 'Córdoba'},
        {'cp': 'M5500', 'nombre': 'Mendoza'},
        {'cp': 'S3000', 'nombre': 'Santa Fe'},
        {'cp': 'R2000', 'nombre': 'Rosario'},
    ]
    localidades = []
    for data in localidades_data:
        localidad, created = Localidad.objects.get_or_create(
            cp=data['cp'], defaults={'nombre': data['nombre']}
        )
        if created:
            print(f"Created Localidad: {localidad}")
        localidades.append(localidad)

    # Insumo data (cleaning supplies)
    insumos_data = [
        {'descripcion': 'Detergente Líquido', 'unidad_med': 4, 'contenido_neto': 5, 'marca': 'LimpiaMax', 'cantidad': 50},
        {'descripcion': 'Desinfectante', 'unidad_med': 4, 'contenido_neto': 1, 'marca': 'Sanit', 'cantidad': 100},
        {'descripcion': 'Limpiavidrios', 'unidad_med': 3, 'contenido_neto': 500, 'marca': 'Cristal', 'cantidad': 80},
        {'descripcion': 'Jabón en Polvo', 'unidad_med': 2, 'contenido_neto': 3, 'marca': 'Puro', 'cantidad': 40},
        {'descripcion': 'Cera para Pisos', 'unidad_med': 4, 'contenido_neto': 2, 'marca': 'Brillo', 'cantidad': 60},
        {'descripcion': 'Perfumante', 'unidad_med': 3, 'contenido_neto': 250, 'marca': 'Aroma', 'cantidad': 70},
        {'descripcion': 'Blanqueador', 'unidad_med': 4, 'contenido_neto': 1, 'marca': 'Cloro', 'cantidad': 90},
        {'descripcion': 'Esponjas', 'unidad_med': 1, 'contenido_neto': 10, 'marca': 'Scrub', 'cantidad': 200},
        {'descripcion': 'Guantes de Látex', 'unidad_med': 1, 'contenido_neto': 100, 'marca': 'Protect', 'cantidad': 150},
        {'descripcion': 'Trapos de Microfibra', 'unidad_med': 1, 'contenido_neto': 50, 'marca': 'Clean', 'cantidad': 120},
    ]
    insumos = []
    for data in insumos_data:
        insumo, created = Insumo.objects.get_or_create(
            descripcion=data['descripcion'],
            unidad_med=data['unidad_med'],
            contenido_neto=data['contenido_neto'],
            marca=data['marca'],
            defaults={'cantidad': data['cantidad'], 'activo': True}
        )
        if created:
            print(f"Created Insumo: {insumo}")
        insumos.append(insumo)

    # Maquinaria data (cleaning equipment)
    maquinarias_data = [
        {'nombre': 'Aspiradora Industrial', 'modelo': 'CleanPro 3000', 'marca': 'CleanTech', 'cantidad': 5, 'observaciones': 'Alta potencia'},
        {'nombre': 'Pulidora de Pisos', 'modelo': 'ShineX 500', 'marca': 'BrilloMax', 'cantidad': 3, 'observaciones': 'Para mármol y madera'},
        {'nombre': 'Limpiadora a Vapor', 'modelo': 'SteamJet 200', 'marca': 'VaporTech', 'cantidad': 4, 'observaciones': 'Desinfección profunda'},
        {'nombre': 'Hidrolavadora', 'modelo': 'PressurePro 400', 'marca': 'AquaForce', 'cantidad': 2, 'observaciones': 'Alta presión'},
        {'nombre': 'Fregadora Automática', 'modelo': 'ScrubMaster 600', 'marca': 'CleanBot', 'cantidad': 3, 'observaciones': 'Para grandes superficies'},
    ]
    maquinarias = []
    for data in maquinarias_data:
        maquinaria, created = Maquinaria.objects.get_or_create(
            nombre=data['nombre'],
            modelo=data['modelo'],
            marca=data['marca'],
            defaults={'cantidad': data['cantidad'], 'observaciones': data['observaciones'], 'activo': True}
        )
        if created:
            print(f"Created Maquinaria: {maquinaria}")
        maquinarias.append(maquinaria)

    # TipoServicio data (cleaning services)
    tipos_servicio_data = [
        {'descripcion': 'Limpieza de Oficinas', 'unidad_medida': 1, 'precio': 5000},
        {'descripcion': 'Desinfección de Baños', 'unidad_medida': 2, 'precio': 3000},
        {'descripcion': 'Limpieza de Vidrios', 'unidad_medida': 2, 'precio': 4000},
        {'descripcion': 'Pulido de Pisos', 'unidad_medida': 1, 'precio': 6000},
        {'descripcion': 'Limpieza General', 'unidad_medida': 1, 'precio': 4500},
    ]
    tipos_servicio = []
    for data in tipos_servicio_data:
        tipo_servicio, created = TipoServicio.objects.get_or_create(
            descripcion=data['descripcion'],
            unidad_medida=data['unidad_medida'],
            defaults={'precio': data['precio'], 'activo': True}
        )
        if created:
            print(f"Created TipoServicio: {tipo_servicio}")
            # Assign random insumos and maquinarias
            tipo_servicio.insumos.set(random.sample(insumos, k=random.randint(2, 5)))
            tipo_servicio.maquinarias.set(random.sample(maquinarias, k=random.randint(1, 3)))
            # Create CantInsumoServicio entries
            for insumo in tipo_servicio.insumos.all():
                CantInsumoServicio.objects.get_or_create(
                    insumo=insumo,
                    tipoServicio=tipo_servicio,
                    defaults={'cantidad': random.randint(1, 10)}
                )
        tipos_servicio.append(tipo_servicio)

    # Cliente data (motorsport pilots)
    clientes_data = [
        {'nombre': 'Juan Manuel', 'apellido': 'Fangio', 'dni': '45123789', 'cuil_prefix': '20'},
        {'nombre': 'Ángel', 'apellido': 'Di María', 'dni': '32456123', 'cuil_prefix': '20'},
        {'nombre': 'Gabriel', 'apellido': 'Ponce de León', 'dni': '28789456', 'cuil_prefix': '20'},
        {'nombre': 'María', 'apellido': 'López', 'dni': '19234567', 'cuil_prefix': '27'},  # Fictional female pilot
        {'nombre': 'Ayrton', 'apellido': 'Senna', 'dni': '41678901', 'cuil_prefix': '20'},
        {'nombre': 'Lewis', 'apellido': 'Hamilton', 'dni': '36901234', 'cuil_prefix': '20'},
        {'nombre': 'Michael', 'apellido': 'Schumacher', 'dni': '25567890', 'cuil_prefix': '20'},
        {'nombre': 'Valentina', 'apellido': 'Gómez', 'dni': '47123456', 'cuil_prefix': '27'},  # Fictional female pilot
        {'nombre': 'José María', 'apellido': 'López', 'dni': '33890123', 'cuil_prefix': '20'},
        {'nombre': 'Sebastian', 'apellido': 'Vettel', 'dni': '29456789', 'cuil_prefix': '20'},
    ]
    for i, data in enumerate(clientes_data):
        cuil = f"{data['cuil_prefix']}-{data['dni']}-{random.randint(0, 9)}"
        cliente, created = Cliente.objects.get_or_create(
            cuil=cuil,
            defaults={
                'nombre': data['nombre'],
                'apellido': data['apellido'],
                'direccion': f'Calle {i+1} 123',
                'tipo': random.choice([1, 2]),  # Ocacional or Habitual
                'tipoPersona': random.choice([1, 2]),  # Particular or Juridico
                'telefono': f'11{random.randint(10000000, 99999999)}',
                'email': f"{data['nombre'].lower()}.{data['apellido'].lower()}@example.com".replace(' ', ''),
                'localidad': random.choice(localidades),
                'activo': True
            }
        )
        if created:
            print(f"Created Cliente: {cliente}")

    # Empleado data (motorsport pilots)
    empleados_data = [
        {'nombre': 'Oscar', 'apellido': 'Gálvez', 'dni': '45123789'},
        {'nombre': 'Juan', 'apellido': 'Gálvez', 'dni': '32456123'},
        {'nombre': 'Matías', 'apellido': 'Rossi', 'dni': '28789456'},
        {'nombre': 'Sofía', 'apellido': 'Martínez', 'dni': '19234567'},  # Fictional female pilot
        {'nombre': 'Alain', 'apellido': 'Prost', 'dni': '41678901'},
        {'nombre': 'Fernando', 'apellido': 'Alonso', 'dni': '36901234'},
        {'nombre': 'Kimi', 'apellido': 'Räikkönen', 'dni': '25567890'},
        {'nombre': 'Carla', 'apellido': 'Pérez', 'dni': '47123456'},  # Fictional female pilot
        {'nombre': 'Leonel', 'apellido': 'Pernía', 'dni': '33890123'},
        {'nombre': 'Max', 'apellido': 'Verstappen', 'dni': '29456789'},
    ]
    for data in empleados_data:
        empleado, created = Empleado.objects.get_or_create(
            numDNI=data['dni'],
            defaults={
                'nombre': data['nombre'],
                'apellido': data['apellido'],
                'telefono': f'11{random.randint(10000000, 99999999)}',
                'email': f"{data['nombre'].lower()}.{data['apellido'].lower()}@example.com".replace(' ', ''),
                'sueldo': 58000 + random.randint(20000, 100000),  # sueldo_basico + extra
                'localidad': random.choice(localidades),
                'activo': True
            }
        )
        if created:
            print(f"Created Empleado: {empleado} (Sueldo: {empleado.getSueldoFormateado()})")

if __name__ == '__main__':
    print("Populating database...")
    populate_data()
    print("Database population complete.")