# Script para cargar empleados con nombres de pilotos de automovilismo
# Ejecutar en Django shell: python manage.py shell

import random
from faker import Faker
from core.models import (
    Empleado,
    Localidad,
    Cliente,
    Insumo,
    Maquinaria,
    TipoServicio,
    CantInsumoServicio,
)  # Ajusta 'myapp' al nombre de tu app

fake = Faker("es_ES")

# Lista de pilotos de automovilismo (nombres sin acentos ni espacios)
pilotos = [
    # Pilotos argentinos
    ("Juan", "Fangio"),
    ("Carlos", "Reutemann"),
    ("Jose", "Froilan"),
    ("Gaston", "Mazzacane"),
    ("Esteban", "Tuero"),
    ("Agustin", "Canapino"),
    ("Emilio", "Satriano"),
    ("Oscar", "Galvez"),
    ("Guillermo", "Ortelli"),
    ("Mariano", "Werner"),
    ("Matias", "Rossi"),
    ("Christian", "Ledesma"),
    ("Omar", "Martinez"),
    ("Norberto", "Fontana"),
    ("Diego", "Aventin"),
    # Pilotos extranjeros famosos
    ("Lewis", "Hamilton"),
    ("Max", "Verstappen"),
    ("Charles", "Leclerc"),
    ("Lando", "Norris"),
    ("George", "Russell"),
    ("Carlos", "Sainz"),
    ("Sergio", "Perez"),
    ("Fernando", "Alonso"),
    ("Sebastian", "Vettel"),
    ("Michael", "Schumacher"),
    ("Ayrton", "Senna"),
    ("Alain", "Prost"),
    ("Niki", "Lauda"),
    ("Jackie", "Stewart"),
    ("Jim", "Clark"),
    ("Kimi", "Raikkonen"),
    ("Daniel", "Ricciardo"),
    ("Valtteri", "Bottas"),
    ("Pierre", "Gasly"),
    ("Esteban", "Ocon"),
    ("Lance", "Stroll"),
    ("Yuki", "Tsunoda"),
    ("Alexander", "Albon"),
    ("Kevin", "Magnussen"),
    ("Nico", "Hulkenberg"),
    ("Zhou", "Guanyu"),
    ("Oscar", "Piastri"),
    ("Logan", "Sargeant"),
    ("Nyck", "DeVries"),
    ("Mick", "Schumacher"),
]

# Lista de nombres para clientes (más variados)
nombres_clientes = [
    "Adrian",
    "Alberto",
    "Alejandro",
    "Ana",
    "Andrea",
    "Angel",
    "Antonio",
    "Beatriz",
    "Carlos",
    "Carmen",
    "Cristina",
    "Daniel",
    "David",
    "Diego",
    "Eduardo",
    "Elena",
    "Francisco",
    "Gabriel",
    "Gonzalo",
    "Guillermo",
    "Hector",
    "Isabel",
    "Javier",
    "Jesus",
    "Jorge",
    "Jose",
    "Juan",
    "Laura",
    "Luis",
    "Manuel",
    "Maria",
    "Mario",
    "Miguel",
    "Natalia",
    "Nicolas",
    "Pablo",
    "Patricia",
    "Pedro",
    "Rafael",
    "Ramon",
    "Ricardo",
    "Roberto",
    "Rosa",
    "Sandra",
    "Santiago",
    "Sofia",
    "Teresa",
    "Victor",
]

apellidos_clientes = [
    "Alvarez",
    "Blanco",
    "Castro",
    "Diaz",
    "Fernandez",
    "Garcia",
    "Gonzalez",
    "Gutierrez",
    "Hernandez",
    "Jimenez",
    "Lopez",
    "Martin",
    "Martinez",
    "Morales",
    "Moreno",
    "Munoz",
    "Navarro",
    "Ortega",
    "Perez",
    "Ramirez",
    "Ramos",
    "Rodriguez",
    "Romero",
    "Ruiz",
    "Sanchez",
    "Silva",
    "Torres",
    "Vargas",
    "Vazquez",
    "Vega",
    "Acosta",
    "Aguilar",
    "Cabrera",
    "Delgado",
    "Espinosa",
    "Flores",
    "Herrera",
    "Mendoza",
    "Molina",
    "Pena",
    "Rios",
    "Rojas",
    "Soto",
    "Suarez",
    "Valdez",
]

# Productos de limpieza para insumos
productos_limpieza = [
    # Limpiadores multiuso
    "Limpiador Multiusos",
    "Desinfectante",
    "Limpiador de Vidrios",
    "Limpiador de Baños",
    "Limpiador de Cocina",
    "Removedor de Grasa",
    # Detergentes
    "Detergente Liquido",
    "Detergente en Polvo",
    "Detergente Concentrado",
    "Detergente Industrial",
    "Detergente para Ropa",
    "Detergente Biodegradable",
    # Desinfectantes
    "Alcohol Etilico",
    "Alcohol Isopropilico",
    "Lavandina",
    "Hipoclorito de Sodio",
    "Amonio Cuaternario",
    "Desinfectante Hospitalario",
    "Sanitizante",
    # Jabones
    "Jabon Liquido",
    "Jabon en Espuma",
    "Jabon Antibacterial",
    "Jabon Industrial",
    "Jabon para Manos",
    "Jabon Neutro",
    # Productos especializados
    "Cera para Pisos",
    "Lustrador",
    "Desincrustante",
    "Quitamanchas",
    "Blanqueador",
    "Suavizante",
    "Limpiador de Alfombras",
    "Shampoo de Tapiceria",
    # Acidos y bases
    "Acido Muriatico",
    "Soda Caustica",
    "Bicarbonato de Sodio",
    "Vinagre Blanco",
    "Acido Citrico",
    "Amoníaco",
    # Solventes
    "Alcohol en Gel",
    "Acetona",
    "Aguarras",
    "Thinner",
    "Varsol",
    # Productos para mantenimiento
    "Cera Liquida",
    "Cera en Pasta",
    "Sellador de Pisos",
    "Renovador de Plasticos",
    "Limpiador de Metales",
    "Antioxidante",
    "Pulidor de Acero",
    # Aromatizantes y desodorantes
    "Aromatizante Ambiental",
    "Desodorante de Ambiente",
    "Neutralizador de Olores",
    "Perfume Textil",
    "Esencia Floral",
]

marcas_limpieza = [
    "Mr. Musculo",
    "Ayudin",
    "Procenex",
    "Cif",
    "Skip",
    "Drive",
    "Ala",
    "Magistral",
    "Queenax",
    "Sapolio",
    "Zorro",
    "Fabuloso",
    "Lysoform",
    "Raid",
    "Glade",
    "Blem",
    "Rex",
    "Conejo",
    "Ajax",
    "Vim",
    "Detex",
    "Professional",
    "Industrial Clean",
    "EcoClean",
    "ChemiClean",
    "ProLimpia",
]

# Listas de maquinarias de limpieza - Agregar después de las listas existentes
maquinarias_nombres = [
    "Aspiradora Industrial",
    "Hidrolavadora",
    "Enceradadora",
    "Pulidora de Pisos",
    "Limpiadora de Alfombras",
    "Aspiradora en Seco",
    "Aspiradora Agua-Polvo",
    "Brilladora",
    "Fregadora",
    "Barredora",
    "Rotativa",
    "Monodisco",
    "Extractor de Vapor",
    "Limpiadora de Tapizados",
    "Aspiradora de Mano",
    "Sopladora",
    "Generador de Vapor",
    "Limpiadora de Cristales",
    "Secadora",
    "Deshumidificador",
    "Generador de Espuma",
    "Pulverizadora",
    "Nebulizadora",
    "Limpiadora Ultrasónica",
    "Lavadora de Presión",
]

marcas_maquinarias = [
    "Karcher",
    "Lavor",
    "Black & Decker",
    "Bosch",
    "Makita",
    "Nilfisk",
    "Electrolux",
    "Hoover",
    "Bissell",
    "Shark",
    "Dyson",
    "Tineco",
    "Rug Doctor",
    "Craftsman",
    "Ryobi",
    "DeWalt",
    "Milwaukee",
    "Worx",
    "Greenworks",
    "Sun Joe",
    "Simpson",
    "Generac",
    "Briggs & Stratton",
    "Honda",
    "Yamaha",
]

# Modelos genéricos que se pueden combinar con las marcas
modelos_base = [
    "Pro",
    "Max",
    "Ultra",
    "Premium",
    "Industrial",
    "Professional",
    "Heavy Duty",
    "Compact",
    "Deluxe",
    "Standard",
    "Commercial",
    "Turbo",
    "Power",
    "Elite",
    "Advanced",
    "Classic",
    "Series",
    "Force",
    "Master",
    "Supreme",
]

# Números de modelo
numeros_modelo = [
    "1000",
    "1200",
    "1500",
    "2000",
    "2500",
    "3000",
    "X1",
    "X2",
    "X3",
    "V8",
    "V10",
    "V12",
    "HD",
    "XL",
    "XXL",
    "Mini",
    "Maxi",
    "Plus",
    "Super",
    "Mega",
]

observaciones_maquinarias = [
    "Funciona correctamente, mantenimiento al día",
    "Requiere cambio de filtros próximamente",
    "Excelente estado, comprada recientemente",
    "Necesita servicio técnico menor",
    "En perfecto estado de funcionamiento",
    "Requiere lubricación de partes móviles",
    "Funcional, con uso intensivo",
    "Impecable, poco uso",
    "Operativa, revisar cables de alimentación",
    "Buen estado general, uso moderado",
    "Excelente rendimiento, sin observaciones",
    "Funciona bien, ruido normal de funcionamiento",
    "Estado óptimo, garantía vigente",
    "Operativa, programar mantenimiento preventivo",
    "Sin observaciones, funcionamiento normal",
    "Requiere limpieza profunda",
    "Funcional, cambiar accesorios gastados",
    "Perfecto estado, recién calibrada",
    "Operativa, verificar presión de trabajo",
    "Excelente estado, almacenada correctamente",
]

# Lista base de servicios de limpieza
servicios_limpieza = [
    "Limpieza de Alfombras",
    "Limpieza de Tapizados",
    "Limpieza de Escaleras",
    "Limpieza de Oficinas",
    "Limpieza de Vidrios",
    "Limpieza de Cocinas Industriales",
    "Desinfección General",
    "Pulido de Pisos",
    "Lavado de Cortinas",
    "Limpieza de Baños Públicos",
    "Sanitización de Ambientes",
    "Limpieza Post Obra",
    "Limpieza de Garajes",
    "Limpieza de Fachadas",
    "Lavado de Alfombras en Seco",
]


def crear_tipos_servicio():
    """Crear tipos de servicio con insumos y maquinarias relacionados"""
    tipos_creados = 0
    tipos_omitidos = 0

    insumos_disponibles = list(Insumo.objects.all())
    maquinarias_disponibles = list(Maquinaria.objects.all())

    if not insumos_disponibles:
        print("❌ No hay insumos disponibles. Crear insumos primero.")
        return

    if not maquinarias_disponibles:
        print("❌ No hay maquinarias disponibles. Crear maquinarias primero.")
        return

    for nombre_servicio in servicios_limpieza:
        if TipoServicio.objects.filter(descripcion=nombre_servicio).exists():
            print(f"Servicio ya existe: {nombre_servicio} - OMITIDO")
            tipos_omitidos += 1
            continue

        try:
            unidad = random.choice([1, 2])  # m2 o unidad
            precio = random.randint(2000, 15000)

            tipo_servicio = TipoServicio.objects.create(
                descripcion=nombre_servicio,
                unidad_medida=unidad,
                precio=precio,
                activo=random.choice([True] * 9 + [False]),
            )

            # Relacionar con 2 a 4 insumos aleatorios y cantidades
            insumos_relacionados = random.sample(
                insumos_disponibles, k=random.randint(2, 4)
            )
            for insumo in insumos_relacionados:
                cantidad = random.randint(1, 10)
                CantInsumoServicio.objects.create(
                    insumo=insumo,
                    tipoServicio=tipo_servicio,
                    cantidad=cantidad,
                )

            # Relacionar con 1 o 2 maquinarias aleatorias
            maquinarias_relacionadas = random.sample(
                maquinarias_disponibles, k=random.randint(1, 2)
            )
            tipo_servicio.maquinarias.set(maquinarias_relacionadas)

            print(f"✅ Tipo de servicio creado: {nombre_servicio}")
            tipos_creados += 1

        except Exception as e:
            print(f"❌ Error creando servicio {nombre_servicio}: {str(e)}")

    print("\n=== RESUMEN ===")
    print(f"Servicios creados: {tipos_creados}")
    print(f"Servicios omitidos (ya existían): {tipos_omitidos}")


def crear_localidades_chubut():
    """Crea localidades reales de la provincia del Chubut con sus respectivos códigos postales"""
    localidades_chubut = [
        ("Rawson", "9103"),
        ("Trelew", "9100"),
        ("Puerto Madryn", "9120"),
        ("Comodoro Rivadavia", "9000"),
        ("Esquel", "9200"),
        ("Gaiman", "9105"),
        ("Dolavon", "9107"),
        ("Paso de Indios", "9225"),
        ("Gobernador Costa", "9223"),
        ("Sarmiento", "9107"),
        ("Rada Tilly", "9001"),
        ("Camarones", "9111"),
        ("Lago Puelo", "9211"),
        ("El Maitén", "9210"),
        ("Epuyén", "9211"),
        ("Cholila", "9217"),
        ("Tecka", "9201"),
        ("José de San Martín", "9220"),
        ("Alto Río Senguer", "9033"),
        ("Río Mayo", "9030"),
        ("Río Pico", "9221"),
        ("Carrenleufú", "9227"),
        ("Corcovado", "9222"),
        ("Las Plumas", "9221"),
        ("Telsen", "9121"),
        ("Gan Gan", "9127"),
        ("Paso del Sapo", "9225"),
        ("Colán Conhué", "9221"),
    ]

    creadas = 0
    omitidas = 0

    for nombre, cp in localidades_chubut:
        try:
            if Localidad.objects.filter(cp=cp).exists():
                print(f"Localidad ya existe: {nombre} ({cp}) - OMITIDA")
                omitidas += 1
                continue

            localidad = Localidad(nombre=nombre, cp=cp)
            localidad.save()
            print(f"Localidad creada: {nombre} ({cp})")
            creadas += 1
        except Exception as e:
            print(f"Error creando localidad {nombre}: {str(e)}")

    print(f"\n✔ Localidades creadas: {creadas}")
    print(f"ℹ Localidades omitidas (ya existían): {omitidas}")


def crear_maquinarias(cantidad=15):
    """Función para crear maquinarias de limpieza con datos aleatorios"""

    maquinarias_creadas = 0
    maquinarias_ya_existentes = 0

    for i in range(cantidad):
        try:
            # Seleccionar nombre y marca aleatoriamente
            nombre = random.choice(maquinarias_nombres)
            marca = random.choice(marcas_maquinarias)

            # Generar modelo combinando elementos aleatorios
            modelo_parte1 = random.choice(modelos_base)
            modelo_parte2 = random.choice(numeros_modelo)
            modelo = f"{modelo_parte1} {modelo_parte2}"

            # Verificar si ya existe una maquinaria con este nombre, marca y modelo
            if Maquinaria.objects.filter(
                nombre=nombre, marca=marca, modelo=modelo
            ).exists():
                print(f"Maquinaria ya existe: {nombre} - {marca} {modelo} - OMITIDO")
                maquinarias_ya_existentes += 1
                continue

            # Cantidad aleatoria (1-5 unidades por maquinaria)
            cantidad_maq = random.randint(1, 5)

            # Observaciones aleatorias
            observaciones = random.choice(observaciones_maquinarias)

            # Estado aleatorio (85% activas)
            activo = random.choice([True] * 17 + [False] * 3)

            # Crear maquinaria
            maquinaria = Maquinaria(
                nombre=nombre,
                modelo=modelo,
                marca=marca,
                cantidad=cantidad_maq,
                observaciones=observaciones,
                activo=activo,
            )

            maquinaria.save()
            maquinarias_creadas += 1

            estado_texto = "Activa" if activo else "Inactiva"
            print(
                f"Maquinaria creada: {nombre} - {marca} {modelo} - Cant: {cantidad_maq} - {estado_texto}"
            )

        except Exception as e:
            print(f"Error creando maquinaria {nombre} - {marca}: {str(e)}")

    print(f"\n¡Proceso completado!")
    print(f"Maquinarias creadas: {maquinarias_creadas}")
    print(f"Maquinarias omitidas (ya existían): {maquinarias_ya_existentes}")


def limpiar_maquinarias():
    """Función para eliminar todas las maquinarias existentes"""
    count = Maquinaria.objects.count()

    if count == 0:
        print("No hay maquinarias para eliminar.")
        return

    print(f"Hay {count} maquinarias en la base de datos.")
    confirmacion = input(
        "¿Estás seguro de que quieres eliminar todas las maquinarias? (si/no): "
    )

    if confirmacion.lower() in ["si", "s", "yes", "y"]:
        Maquinaria.objects.all().delete()
        print(f"Se eliminaron {count} maquinarias exitosamente.")
    else:
        print("Operación cancelada.")


def limpiar_maquinarias_script():
    """Función para eliminar solo las maquinarias creadas por este script"""
    maquinarias_script = Maquinaria.objects.filter(
        nombre__in=maquinarias_nombres, marca__in=marcas_maquinarias
    )

    count = maquinarias_script.count()

    if count == 0:
        print("No hay maquinarias del script para eliminar.")
        return

    print(f"Se encontraron {count} maquinarias creadas por el script:")
    for maquinaria in maquinarias_script[:5]:  # Mostrar solo las primeras 5
        print(f"  - {maquinaria.nombre} ({maquinaria.marca} {maquinaria.modelo})")

    if count > 5:
        print(f"  ... y {count - 5} más.")

    confirmacion = input("¿Eliminar estas maquinarias? (si/no): ")

    if confirmacion.lower() in ["si", "s", "yes", "y"]:
        maquinarias_script.delete()
        print(f"Se eliminaron {count} maquinarias exitosamente.")
    else:
        print("Operación cancelada.")


def mostrar_ejemplos_maquinarias():
    """Muestra algunas maquinarias creadas como ejemplo"""
    maquinarias = Maquinaria.objects.all()[:5]
    print("\n=== Ejemplos de maquinarias creadas ===")
    for maquinaria in maquinarias:
        print(f"- {maquinaria.nombre}")
        print(f"  Marca: {maquinaria.marca}")
        print(f"  Modelo: {maquinaria.modelo}")
        print(f"  Cantidad: {maquinaria.cantidad}")
        print(f"  Estado: {'Activa' if maquinaria.activo else 'Inactiva'}")
        print(f"  Observaciones: {maquinaria.observaciones}")
        print()


def crear_insumos(cantidad=25):
    """Función para crear insumos de limpieza con datos aleatorios"""

    insumos_creados = 0
    insumos_ya_existentes = 0

    for i in range(cantidad):
        try:
            # Seleccionar producto y marca aleatoriamente
            descripcion = random.choice(productos_limpieza)
            marca = random.choice(marcas_limpieza)

            # Verificar si ya existe un insumo con esta descripción y marca
            if Insumo.objects.filter(descripcion=descripcion, marca=marca).exists():
                print(f"Insumo ya existe: {descripcion} - {marca} - OMITIDO")
                insumos_ya_existentes += 1
                continue

            # Unidad de medida según el tipo de producto
            if any(
                palabra in descripcion.lower()
                for palabra in [
                    "liquido",
                    "alcohol",
                    "vinagre",
                    "acido",
                    "gel",
                    "varsol",
                    "acetona",
                    "aguarras",
                    "thinner",
                ]
            ):
                # Productos líquidos: ml o Lts
                unidad_med = random.choice([3, 4])  # ml o Lts
                if unidad_med == 3:  # ml
                    contenido_neto = random.choice([250, 500, 750, 1000])
                else:  # Lts
                    contenido_neto = random.choice([1, 2, 5, 10, 20])
            else:
                # Productos sólidos/polvo: gr o Kg
                unidad_med = random.choice([1, 2])  # gr o Kg
                if unidad_med == 1:  # gr
                    contenido_neto = random.choice([500, 750, 1000])
                else:  # Kg
                    contenido_neto = random.choice([1, 2, 5, 10, 25])

            # Cantidad en stock (aleatorio entre 5 y 100)
            cantidad = random.randint(5, 100)

            # Estado aleatorio (90% activos)
            activo = random.choice([True] * 9 + [False])

            # Crear insumo
            insumo = Insumo(
                descripcion=descripcion,
                unidad_med=unidad_med,
                contenido_neto=contenido_neto,
                marca=marca,
                cantidad=cantidad,
                activo=activo,
            )

            insumo.save()
            insumos_creados += 1

            unidad_texto = insumo.getUni_Medida()
            estado_texto = "Activo" if activo else "Inactivo"
            print(
                f"Insumo creado: {descripcion} ({marca}) - {contenido_neto}{unidad_texto} - Stock: {cantidad} - {estado_texto}"
            )

        except Exception as e:
            print(f"Error creando insumo {descripcion} - {marca}: {str(e)}")

    print(f"\n¡Proceso completado!")
    print(f"Insumos creados: {insumos_creados}")
    print(f"Insumos omitidos (ya existían): {insumos_ya_existentes}")


def limpiar_insumos():
    """Función para eliminar todos los insumos existentes"""
    count = Insumo.objects.count()

    if count == 0:
        print("No hay insumos para eliminar.")
        return

    print(f"Hay {count} insumos en la base de datos.")
    confirmacion = input(
        "¿Estás seguro de que quieres eliminar todos los insumos? (si/no): "
    )

    if confirmacion.lower() in ["si", "s", "yes", "y"]:
        Insumo.objects.all().delete()
        print(f"Se eliminaron {count} insumos exitosamente.")
    else:
        print("Operación cancelada.")


def limpiar_insumos_script():
    """Función para eliminar solo los insumos creados por este script"""
    insumos_script = Insumo.objects.filter(
        descripcion__in=productos_limpieza, marca__in=marcas_limpieza
    )

    count = insumos_script.count()

    if count == 0:
        print("No hay insumos del script para eliminar.")
        return

    print(f"Se encontraron {count} insumos creados por el script:")
    for insumo in insumos_script[:5]:  # Mostrar solo los primeros 5
        print(f"  - {insumo.descripcion} ({insumo.marca})")

    if count > 5:
        print(f"  ... y {count - 5} más.")

    confirmacion = input("¿Eliminar estos insumos? (si/no): ")

    if confirmacion.lower() in ["si", "s", "yes", "y"]:
        insumos_script.delete()
        print(f"Se eliminaron {count} insumos exitosamente.")
    else:
        print("Operación cancelada.")


def mostrar_ejemplos_insumos():
    """Muestra algunos insumos creados como ejemplo"""
    insumos = Insumo.objects.all()[:5]
    print("\n=== Ejemplos de insumos creados ===")
    for insumo in insumos:
        print(f"- {insumo.descripcion}")
        print(f"  Marca: {insumo.marca}")
        print(f"  Contenido: {insumo.contenido_neto} {insumo.getUni_Medida()}")
        print(f"  Stock: {insumo.cantidad}")
        print(f"  Estado: {insumo.getEstado()}")
        print()


def crear_clientes(cantidad=30):
    """Función para crear clientes con datos aleatorios"""

    # Verificar que existan localidades
    localidades = list(Localidad.objects.all())
    if not localidades:
        print(
            "Error: No hay localidades en la base de datos. Crear al menos una localidad primero."
        )
        return

    clientes_creados = 0
    clientes_ya_existentes = 0

    for i in range(cantidad):
        try:
            # Generar nombres aleatorios
            nombre = random.choice(nombres_clientes)
            apellido = random.choice(apellidos_clientes)

            # Verificar si ya existe un cliente con este nombre y apellido
            if Cliente.objects.filter(nombre=nombre, apellido=apellido).exists():
                print(f"Cliente ya existe: {nombre} {apellido} - OMITIDO")
                clientes_ya_existentes += 1
                continue

            # Generar CUIL único (formato: XX-XXXXXXXX-X)
            cuil_base = fake.unique.random_number(digits=11, fix_len=True)
            cuil = f"{str(cuil_base)[:2]}-{str(cuil_base)[2:10]}-{str(cuil_base)[10]}"

            # Generar datos aleatorios
            direccion = fake.address()[:50]  # Limitar a 50 caracteres
            telefono = fake.phone_number()[:10]  # Limitar a 10 caracteres
            email = f"{nombre.lower()}.{apellido.lower()}@{random.choice(['gmail', 'yahoo', 'hotmail', 'outlook'])}.com"

            # Tipo de cliente: 70% Ocasional, 30% Habitual
            tipo = random.choice([1] * 7 + [2] * 3)

            # Tipo de persona: 80% Particular, 20% Jurídico
            tipoPersona = random.choice([1] * 8 + [2] * 2)

            # Seleccionar localidad aleatoria
            localidad = random.choice(localidades)

            # Estado aleatorio (95% activos)
            activo = random.choice([True] * 19 + [False])

            # Crear cliente
            cliente = Cliente(
                nombre=nombre,
                apellido=apellido,
                direccion=direccion,
                tipo=tipo,
                tipoPersona=tipoPersona,
                cuil=cuil,
                telefono=telefono,
                email=email,
                localidad=localidad,
                activo=activo,
            )

            cliente.save()
            clientes_creados += 1

            tipo_texto = "Ocasional" if tipo == 1 else "Habitual"
            persona_texto = "Particular" if tipoPersona == 1 else "Jurídico"
            print(
                f"Cliente creado: {nombre} {apellido} - CUIL: {cuil} - {tipo_texto}/{persona_texto}"
            )

        except Exception as e:
            print(f"Error creando cliente {nombre} {apellido}: {str(e)}")

    print(f"\n¡Proceso completado!")
    print(f"Clientes creados: {clientes_creados}")
    print(f"Clientes omitidos (ya existían): {clientes_ya_existentes}")


def crear_empleados():
    """Función para crear 40 empleados con datos de pilotos"""

    # Verificar que existan localidades
    localidades = list(Localidad.objects.all())
    if not localidades:
        print(
            "Error: No hay localidades en la base de datos. Crear al menos una localidad primero."
        )
        return

    # Seleccionar 40 pilotos aleatoriamente
    pilotos_seleccionados = random.sample(pilotos, 40)

    empleados_creados = 0
    empleados_ya_existentes = 0

    for nombre, apellido in pilotos_seleccionados:
        try:
            # Verificar si ya existe un empleado con este nombre y apellido
            if Empleado.objects.filter(nombre=nombre, apellido=apellido).exists():
                print(f"Empleado ya existe: {nombre} {apellido} - OMITIDO")
                empleados_ya_existentes += 1
                continue

            # Generar DNI único
            dni = fake.unique.random_number(digits=8, fix_len=True)

            # Generar datos aleatorios
            telefono = fake.phone_number()[:10]  # Limitar a 10 caracteres
            email = f"{nombre.lower()}.{apellido.lower()}@empresa.com"

            # Sueldo aleatorio entre 100,000 y 500,000 (sin incluir sueldo básico)
            sueldo = random.randint(100000, 500000)

            # Seleccionar localidad aleatoria
            localidad = random.choice(localidades)

            # Estado aleatorio (90% activos)
            activo = random.choice([True] * 9 + [False])

            # Crear empleado
            empleado = Empleado(
                numDNI=str(dni),
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                email=email,
                sueldo=sueldo,
                localidad=localidad,
                activo=activo,
            )

            empleado.save()
            empleados_creados += 1
            print(f"Empleado creado: {nombre} {apellido} - DNI: {dni}")

        except Exception as e:
            print(f"Error creando empleado {nombre} {apellido}: {str(e)}")

    print(f"\n¡Proceso completado!")
    print(f"Empleados creados: {empleados_creados}")
    print(f"Empleados omitidos (ya existían): {empleados_ya_existentes}")


# Función para limpiar empleados existentes
def limpiar_empleados():
    """Función para eliminar todos los empleados existentes"""
    count = Empleado.objects.count()

    if count == 0:
        print("No hay empleados para eliminar.")
        return

    print(f"Hay {count} empleados en la base de datos.")
    confirmacion = input(
        "¿Estás seguro de que quieres eliminar todos los empleados? (si/no): "
    )

    if confirmacion.lower() in ["si", "s", "yes", "y"]:
        Empleado.objects.all().delete()
        print(f"Se eliminaron {count} empleados exitosamente.")
    else:
        print("Operación cancelada.")


# Funciones de limpieza para clientes
def limpiar_clientes():
    """Función para eliminar todos los clientes existentes"""
    count = Cliente.objects.count()

    if count == 0:
        print("No hay clientes para eliminar.")
        return

    print(f"Hay {count} clientes en la base de datos.")
    confirmacion = input(
        "¿Estás seguro de que quieres eliminar todos los clientes? (si/no): "
    )

    if confirmacion.lower() in ["si", "s", "yes", "y"]:
        Cliente.objects.all().delete()
        print(f"Se eliminaron {count} clientes exitosamente.")
    else:
        print("Operación cancelada.")


def limpiar_clientes_script():
    """Función para eliminar solo los clientes creados por este script"""
    clientes_script = Cliente.objects.filter(
        nombre__in=nombres_clientes, apellido__in=apellidos_clientes
    )

    count = clientes_script.count()

    if count == 0:
        print("No hay clientes del script para eliminar.")
        return

    print(f"Se encontraron {count} clientes creados por el script:")
    for cliente in clientes_script[:5]:  # Mostrar solo los primeros 5
        print(f"  - {cliente.nombre} {cliente.apellido}")

    if count > 5:
        print(f"  ... y {count - 5} más.")

    confirmacion = input("¿Eliminar estos clientes? (si/no): ")

    if confirmacion.lower() in ["si", "s", "yes", "y"]:
        clientes_script.delete()
        print(f"Se eliminaron {count} clientes exitosamente.")
    else:
        print("Operación cancelada.")


# Función para limpiar empleados específicos (por nombre)
def limpiar_empleados_pilotos():
    """Función para eliminar solo los empleados que son pilotos de automovilismo"""
    nombres_pilotos = [nombre for nombre, apellido in pilotos]
    apellidos_pilotos = [apellido for nombre, apellido in pilotos]

    empleados_pilotos = Empleado.objects.filter(
        nombre__in=nombres_pilotos, apellido__in=apellidos_pilotos
    )

    count = empleados_pilotos.count()

    if count == 0:
        print("No hay empleados pilotos para eliminar.")
        return

    print(f"Se encontraron {count} empleados que son pilotos de automovilismo:")
    for emp in empleados_pilotos[:5]:  # Mostrar solo los primeros 5
        print(f"  - {emp.nombre} {emp.apellido}")

    if count > 5:
        print(f"  ... y {count - 5} más.")

    confirmacion = input("¿Eliminar estos empleados? (si/no): ")

    if confirmacion.lower() in ["si", "s", "yes", "y"]:
        empleados_pilotos.delete()
        print(f"Se eliminaron {count} empleados pilotos exitosamente.")
    else:
        print("Operación cancelada.")


# Función adicional para mostrar algunos ejemplos
def mostrar_ejemplos():
    """Muestra algunos empleados creados como ejemplo"""
    empleados = Empleado.objects.all()[:5]
    print("\n=== Ejemplos de empleados creados ===")
    for emp in empleados:
        print(f"- {emp.nombre} {emp.apellido}")
        print(f"  DNI: {emp.numDNI}")
        print(f"  Email: {emp.email}")
        print(f"  Sueldo: ${emp.sueldo:,}")
        print(f"  Estado: {emp.getEstado()}")
        print()


def mostrar_ejemplos_clientes():
    """Muestra algunos clientes creados como ejemplo"""
    clientes = Cliente.objects.all()[:5]
    print("\n=== Ejemplos de clientes creados ===")
    for cliente in clientes:
        print(f"- {cliente.nombre} {cliente.apellido}")
        print(f"  CUIL: {cliente.cuil}")
        print(f"  Email: {cliente.email}")
        print(f"  Tipo: {cliente.getTipo()}")
        print(f"  Persona: {cliente.getTipoPersona()}")
        print(f"  Activo: {'Sí' if cliente.activo else 'No'}")
        print()


def mostrar_estadisticas():
    """Muestra estadísticas completas de empleados, clientes e insumos"""
    print("\n=== ESTADÍSTICAS GENERALES ===")

    # Estadísticas de empleados
    total_empleados = Empleado.objects.count()
    empleados_activos = Empleado.objects.filter(activo=True).count()
    empleados_inactivos = Empleado.objects.filter(activo=False).count()

    print(f"\n📋 EMPLEADOS:")
    print(f"  Total: {total_empleados}")
    print(f"  Activos: {empleados_activos}")
    print(f"  Inactivos: {empleados_inactivos}")

    # Estadísticas de clientes
    total_clientes = Cliente.objects.count()
    clientes_activos = Cliente.objects.filter(activo=True).count()
    clientes_inactivos = Cliente.objects.filter(activo=False).count()

    # Clientes por tipo
    clientes_ocasional = Cliente.objects.filter(tipo=1).count()
    clientes_habitual = Cliente.objects.filter(tipo=2).count()

    # Clientes por tipo de persona
    clientes_particular = Cliente.objects.filter(tipoPersona=1).count()
    clientes_juridico = Cliente.objects.filter(tipoPersona=2).count()

    print(f"\n👥 CLIENTES:")
    print(f"  Total: {total_clientes}")
    print(f"  Activos: {clientes_activos}")
    print(f"  Inactivos: {clientes_inactivos}")
    print(f"  Ocasionales: {clientes_ocasional}")
    print(f"  Habituales: {clientes_habitual}")
    print(f"  Particulares: {clientes_particular}")
    print(f"  Jurídicos: {clientes_juridico}")

    # Estadísticas de insumos
    total_insumos = Insumo.objects.count()
    insumos_activos = Insumo.objects.filter(activo=True).count()
    insumos_inactivos = Insumo.objects.filter(activo=False).count()

    # Insumos por unidad de medida
    insumos_gr = Insumo.objects.filter(unidad_med=1).count()
    insumos_kg = Insumo.objects.filter(unidad_med=2).count()
    insumos_ml = Insumo.objects.filter(unidad_med=3).count()
    insumos_lts = Insumo.objects.filter(unidad_med=4).count()

    print(f"\n🧽 INSUMOS:")
    print(f"  Total: {total_insumos}")
    print(f"  Activos: {insumos_activos}")
    print(f"  Inactivos: {insumos_inactivos}")
    print(f"  En gramos: {insumos_gr}")
    print(f"  En kilogramos: {insumos_kg}")
    print(f"  En mililitros: {insumos_ml}")
    print(f"  En litros: {insumos_lts}")


# Actualizar la función mostrar_estadisticas() - agregar esta sección
def mostrar_estadisticas_maquinarias():
    """Extensión para mostrar estadísticas de maquinarias"""
    # Estadísticas de maquinarias
    total_maquinarias = Maquinaria.objects.count()
    maquinarias_activas = Maquinaria.objects.filter(activo=True).count()
    maquinarias_inactivas = Maquinaria.objects.filter(activo=False).count()

    # Total de unidades (suma de cantidades)
    from django.db.models import Sum

    total_unidades = Maquinaria.objects.aggregate(Sum("cantidad"))["cantidad__sum"] or 0

    print(f"\n🔧 MAQUINARIAS:")
    print(f"  Total tipos: {total_maquinarias}")
    print(f"  Total unidades: {total_unidades}")
    print(f"  Activas: {maquinarias_activas}")
    print(f"  Inactivas: {maquinarias_inactivas}")


# Actualizar la función crear_datos_completos()
def crear_datos_completos_con_maquinarias():
    """Crear empleados, clientes, insumos y maquinarias de una vez"""
    print("=== CREANDO DATOS COMPLETOS DE PRUEBA ===")
    print("Creando empleados...")
    crear_empleados()
    print("\nCreando clientes...")
    crear_clientes(30)
    print("\nCreando insumos...")
    crear_insumos(25)
    print("\nCreando maquinarias...")
    crear_maquinarias(15)
    print("\n=== PROCESO COMPLETADO ===")
    mostrar_estadisticas()
    mostrar_estadisticas_maquinarias()


# Actualizar el menú de opciones al final del script
print("\n🔧 OPCIONES PARA MAQUINARIAS:")
print(
    "  crear_maquinarias() - Crear 15 maquinarias de limpieza (cantidad personalizable)"
)
print("  crear_maquinarias(20) - Crear 20 maquinarias")
print("  limpiar_maquinarias() - Eliminar TODAS las maquinarias")
print("  limpiar_maquinarias_script() - Eliminar solo maquinarias del script")
print("  mostrar_ejemplos_maquinarias() - Mostrar algunas maquinarias")
print("  mostrar_estadisticas_maquinarias() - Ver estadísticas de maquinarias")

print("\n📊 OPCIONES GENERALES ACTUALIZADAS:")
print(
    "  crear_datos_completos_con_maquinarias() - Crear empleados + clientes + insumos + maquinarias"
)

print("\n=== EJEMPLOS DE USO CON MAQUINARIAS ===")
print("  # Crear datos completos incluyendo maquinarias:")
print("  crear_datos_completos_con_maquinarias()")
print()
print("  # Crear solo maquinarias:")
print("  crear_maquinarias()")
print("  mostrar_ejemplos_maquinarias()")
print()
print("  # Limpiar todo incluyendo maquinarias:")
print("  limpiar_empleados_pilotos()")
print("  limpiar_clientes_script()")
print("  limpiar_insumos_script()")
print("  limpiar_maquinarias_script()")
print("\n📍 OPCIONES PARA LOCALIDADES:")
print(
    "  crear_localidades_chubut() - Crear localidades reales de Chubut con código postal"
)
print("\n🧼 OPCIONES PARA TIPOS DE SERVICIO:")
print("  crear_tipos_servicio() - Crear tipos de servicio con insumos y maquinarias relacionadas")



mostrar_estadisticas()

# Para ejecutar en Django shell:
# exec(open('path/to/this/script.py').read())
# O copiar y pegar las funciones y ejecutar:
# crear_insumos()
# mostrar_ejemplos_insumos(
