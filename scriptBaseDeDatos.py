import os
import shutil
import psycopg2
import subprocess
import sys
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*60)
    print("    🧹 SCRIPT DE LIMPIEZA DE PROYECTO DJANGO 🧹")
    print("="*60)
    print("\n📋 OPCIONES DISPONIBLES:")
    print("   1️⃣  Limpiar carpetas de migraciones y cache")
    print("   2️⃣  Vaciar base de datos Supabase (PostgreSQL)")
    print("   3️⃣  Eliminar base de datos SQLite local")
    print("   4️⃣  Limpieza completa (migraciones + base de datos)")
    print("   5️⃣  Solo mostrar información del proyecto")
    print("   6️⃣  Reparar conflictos de migración Django/Supabase")
    print("   7️⃣  Aplicar migraciones y crear superusuario")
    print("   8️⃣  Solo crear superusuario")
    print("   0️⃣  Salir")
    print("="*60)


def borrar_contenido(carpeta):
    """Borra el contenido de una carpeta manteniendo __init__.py"""
    if os.path.exists(carpeta) and os.path.isdir(carpeta):
        archivos_eliminados = 0
        carpetas_eliminadas = 0
        
        for elemento in os.listdir(carpeta):
            path = os.path.join(carpeta, elemento)
            if path.endswith("__init__.py"):
                continue
                         
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)  
                archivos_eliminados += 1
                print(f"   📄 Archivo eliminado: {path}")
            elif os.path.isdir(path):
                shutil.rmtree(path) 
                carpetas_eliminadas += 1
                print(f"   📁 Carpeta eliminada: {path}")
        
        if archivos_eliminados == 0 and carpetas_eliminadas == 0:
            print(f"   ✨ '{carpeta}' ya está limpia")
        else:
            print(f"   ✅ '{carpeta}': {archivos_eliminados} archivos y {carpetas_eliminadas} carpetas eliminadas")
    else:
        print(f"   ⚠️  La carpeta no existe: {carpeta}")


def limpiar_migraciones():
    """Limpia las carpetas de migraciones y cache"""
    print("\n🧹 LIMPIANDO CARPETAS DE MIGRACIONES Y CACHE...")
    print("-" * 50)
    
    carpetas_migrations = [
        "core/migrations",
        "core/__pycache__",
        "servicio/migrations", 
        "servicio/__pycache__",
        "factura/migrations",
        "factura/__pycache__"
    ]
    
    for carpeta in carpetas_migrations:
        borrar_contenido(carpeta)
    
    print("\n✨ Limpieza de carpetas completada!")
    return True


def vaciar_base_datos_supabase():
    """Vacía todas las tablas de la base de datos Supabase"""
    print("\n🗄️  VACIANDO BASE DE DATOS SUPABASE...")
    print("-" * 50)
    
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ ERROR: No se encontró DATABASE_URL en las variables de entorno")
        return False
    
    try:
        # Parsear la URL de conexión
        parsed_url = urlparse(database_url)
        
        # Configuración de conexión
        conn_config = {
            'host': parsed_url.hostname,
            'port': parsed_url.port or 5432,
            'database': parsed_url.path[1:],  # Remover el '/' inicial
            'user': parsed_url.username,
            'password': parsed_url.password,
            'sslmode': 'require'  # Supabase requiere SSL
        }
        
        print(f"🔌 Conectando a: {parsed_url.hostname}")
        
        # Conectar a la base de datos
        conn = psycopg2.connect(**conn_config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa a Supabase")
        
        # Obtener todas las tablas del schema público
        cursor.execute("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename NOT LIKE 'auth_%'
            AND tablename NOT LIKE 'storage_%'
            AND tablename NOT LIKE 'realtime_%'
            AND tablename NOT LIKE 'supabase_%'
            AND tablename NOT LIKE '_realtime_%'
            ORDER BY tablename;
        """)
        
        tablas = cursor.fetchall()
        
        if not tablas:
            print("ℹ️  No se encontraron tablas para vaciar")
            cursor.close()
            conn.close()
            return True
        
        print(f"\n📋 Se encontraron {len(tablas)} tablas:")
        for i, tabla in enumerate(tablas, 1):
            print(f"   {i:2d}. {tabla[0]}")
        
        # Confirmación
        print(f"\n⚠️  ADVERTENCIA: Se vaciarán TODAS las {len(tablas)} tablas listadas")
        print("   Esta operación NO se puede deshacer")
        
        respuesta = input("\n❓ ¿Continuar? (escriba 'VACIAR' para confirmar): ")
        if respuesta != 'VACIAR':
            print("❌ Operación cancelada por el usuario")
            cursor.close()
            conn.close()
            return False
        
        # Proceso de vaciado
        print(f"\n🔄 Iniciando vaciado de {len(tablas)} tablas...")
        
        # Deshabilitar restricciones temporalmente
        cursor.execute("SET session_replication_role = replica;")
        print("   🔓 Restricciones de clave foránea deshabilitadas")
        
        # Vaciar cada tabla
        tablas_vaciadas = []
        for i, tabla in enumerate(tablas, 1):
            tabla_nombre = tabla[0]
            try:
                cursor.execute(f'TRUNCATE TABLE "{tabla_nombre}" RESTART IDENTITY CASCADE;')
                tablas_vaciadas.append(tabla_nombre)
                print(f"   ✅ [{i:2d}/{len(tablas)}] '{tabla_nombre}' vaciada")
            except Exception as e:
                print(f"   ❌ [{i:2d}/{len(tablas)}] Error en '{tabla_nombre}': {e}")
        
        # Rehabilitar restricciones
        cursor.execute("SET session_replication_role = DEFAULT;")
        print("   🔒 Restricciones de clave foránea rehabilitadas")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        
        print(f"\n🎉 ¡Proceso completado exitosamente!")
        print(f"   📊 {len(tablas_vaciadas)}/{len(tablas)} tablas vaciadas")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ ERROR de PostgreSQL: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR inesperado: {e}")
        return False


def borrar_sqlite_local():
    """Borra la base de datos SQLite local"""
    print("\n🗃️  ELIMINANDO BASE DE DATOS SQLITE LOCAL...")
    print("-" * 50)
    
    db_path = os.getenv("DATABASE_URL")
    if not db_path:
        print("❌ No se encontró DATABASE_URL en las variables de entorno")
        return False
    
    if not os.path.exists(db_path):
        print(f"ℹ️  No existe el archivo: {db_path}")
        return False
    
    # Confirmación
    print(f"📄 Archivo a eliminar: {db_path}")
    respuesta = input("\n❓ ¿Confirmar eliminación? (s/n): ")
    
    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        try:
            os.remove(db_path)
            print(f"✅ Base de datos SQLite eliminada: {db_path}")
            return True
        except Exception as e:
            print(f"❌ Error al eliminar: {e}")
            return False
    else:
        print("❌ Eliminación cancelada")
        return False


def mostrar_informacion():
    """Muestra información del proyecto y configuración"""
    print("\n📊 INFORMACIÓN DEL PROYECTO")
    print("-" * 50)
    
    # Información de la base de datos
    database_url = os.getenv("DATABASE_URL", "No configurada")
    print(f"🗄️  Base de datos: {database_url}")
    
    if database_url.startswith("postgres"):
        parsed_url = urlparse(database_url)
        print(f"   • Tipo: PostgreSQL (Supabase)")
        print(f"   • Host: {parsed_url.hostname}")
        print(f"   • Puerto: {parsed_url.port or 5432}")
        print(f"   • Base de datos: {parsed_url.path[1:]}")
    elif database_url != "No configurada":
        if os.path.exists(database_url):
            size = round(os.path.getsize(database_url) / 1024, 2)
            print(f"   • Tipo: SQLite")
            print(f"   • Tamaño: {size} KB")
            print(f"   • Existe: ✅")
        else:
            print(f"   • Tipo: SQLite")
            print(f"   • Existe: ❌")
    
    # Información de carpetas
    print(f"\n📁 Estado de carpetas:")
    carpetas = [
        "core/migrations", "core/__pycache__",
        "servicio/migrations", "servicio/__pycache__", 
        "factura/migrations", "factura/__pycache__"
    ]
    
    for carpeta in carpetas:
        if os.path.exists(carpeta):
            archivos = len([f for f in os.listdir(carpeta) 
                          if not f.endswith("__init__.py")])
            estado = "🟢 Limpia" if archivos == 0 else f"🟡 {archivos} elementos"
        else:
            estado = "🔴 No existe"
        print(f"   • {carpeta}: {estado}")


def limpieza_completa():
    """Realiza limpieza completa del proyecto"""
    print("\n🚀 LIMPIEZA COMPLETA DEL PROYECTO")
    print("-" * 50)
    print("Esta opción realizará:")
    print("   1. Limpieza de migraciones y cache")
    print("   2. Vaciado/eliminación de base de datos")
    
    respuesta = input("\n❓ ¿Continuar con la limpieza completa? (s/n): ")
    if respuesta.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Limpieza completa cancelada")
        return False
    
    # Limpiar migraciones
    limpiar_migraciones()
    
    # Determinar y limpiar base de datos
    database_url = os.getenv("DATABASE_URL", "")
    
    if database_url.startswith("postgres"):
        print("\n" + "="*50)
        vaciar_base_datos_supabase()
    elif database_url and not database_url.startswith("postgres"):
        print("\n" + "="*50)
        borrar_sqlite_local()
    else:
        print("\nℹ️  No se detectó configuración de base de datos")
    
    print("\n🎉 ¡LIMPIEZA COMPLETA FINALIZADA!")
    print("\n📝 Recuerda ejecutar después:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    
    return True


def reparar_conflictos_django():
    """Repara conflictos entre migraciones Django y tablas existentes en Supabase"""
    print("\n🔧 REPARANDO CONFLICTOS DE MIGRACIÓN DJANGO/SUPABASE")
    print("-" * 50)
    
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url or not database_url.startswith("postgres"):
        print("❌ Esta opción solo funciona con bases de datos PostgreSQL/Supabase")
        return False
    
    print("Esta opción resolverá el error:")
    print("   'relation \"django_content_type\" already exists'")
    print("\nEstrategia:")
    print("   1. Eliminar tablas conflictivas de Django")
    print("   2. Limpiar carpetas de migraciones")
    print("   3. Regenerar migraciones limpias")
    
    respuesta = input("\n❓ ¿Continuar con la reparación? (s/n): ")
    if respuesta.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Reparación cancelada")
        return False
    
    try:
        # Conectar a la base de datos
        parsed_url = urlparse(database_url)
        conn_config = {
            'host': parsed_url.hostname,
            'port': parsed_url.port or 5432,
            'database': parsed_url.path[1:],
            'user': parsed_url.username,
            'password': parsed_url.password,
            'sslmode': 'require'
        }
        
        print(f"\n🔌 Conectando a: {parsed_url.hostname}")
        conn = psycopg2.connect(**conn_config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa")
        
        # Eliminar tablas problemáticas de Django
        tablas_django = [
            'django_migrations',
            'django_content_type', 
            'auth_permission',
            'auth_group',
            'auth_group_permissions',
            'auth_user',
            'auth_user_groups',
            'auth_user_user_permissions',
            'django_admin_log',
            'django_session'
        ]
        
        print(f"\n🗑️  Eliminando tablas conflictivas de Django...")
        tablas_eliminadas = []
        
        for tabla in tablas_django:
            try:
                cursor.execute(f'DROP TABLE IF EXISTS "{tabla}" CASCADE;')
                tablas_eliminadas.append(tabla)
                print(f"   ✅ Tabla '{tabla}' eliminada")
            except Exception as e:
                print(f"   ⚠️  No se pudo eliminar '{tabla}': {e}")
        
        cursor.close()
        conn.close()
        
        print(f"\n✅ {len(tablas_eliminadas)} tablas de Django eliminadas")
        
        # Limpiar migraciones
        print("\n🧹 Limpiando carpetas de migraciones...")
        limpiar_migraciones()
        
        print("\n🎉 ¡Reparación completada!")
        print("\n📝 Ahora ejecuta:")
        print("   python manage.py makemigrations")
        print("   python manage.py migrate")
        print("\n💡 Esto debería resolver el conflicto de migraciones")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ ERROR de PostgreSQL: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR inesperado: {e}")
        return False


def crear_superusuario():
    """Crea un superusuario para Django"""
    print("\n👤 CREAR SUPERUUSUARIO")
    print("-" * 50)
    
    print("¿Cómo quieres crear el superusuario?")
    print("   1. Modo rápido (usuario: architin777, contraseña: architin777)")
    print("   2. Personalizado (elegir usuario y contraseña)")
    
    while True:
        opcion = input("\n🔢 Elige una opción (1-2): ").strip()
        
        if opcion == "1":
            # Modo rápido
            username = "architin777"
            password = "architin777"
            email = "admin@example.com"
            print(f"\n⚡ Creando superusuario rápido: {username}")
            break
            
        elif opcion == "2":
            # Modo personalizado
            print("\n✏️  Configuración personalizada:")
            username = input("   👤 Nombre de usuario: ").strip()
            if not username:
                print("❌ El nombre de usuario no puede estar vacío")
                continue
            
            email = input("   📧 Email (opcional, presiona Enter para usar admin@example.com): ").strip()
            if not email:
                email = "admin@example.com"
            
            import getpass
            password = getpass.getpass("   🔒 Contraseña: ")
            if not password:
                print("❌ La contraseña no puede estar vacía")
                continue
            
            confirm_password = getpass.getpass("   🔒 Confirmar contraseña: ")
            if password != confirm_password:
                print("❌ Las contraseñas no coinciden")
                continue
            
            print(f"\n👤 Creando superusuario: {username}")
            break
        else:
            print("❌ Opción no válida. Elige 1 o 2")
    
    try:
        # Crear el superusuario usando Django shell
        django_code = f"""
from django.contrib.auth import get_user_model
User = get_user_model()

# Verificar si el usuario ya existe
if User.objects.filter(username='{username}').exists():
    print('ADVERTENCIA: El usuario {username} ya existe')
    user = User.objects.get(username='{username}')
    user.set_password('{password}')
    user.save()
    print('Contraseña actualizada')
else:
    user = User.objects.create_superuser(
        username='{username}',
        email='{email}',
        password='{password}'
    )
    print('Superusuario creado exitosamente')

print(f'Usuario: {username}')
print(f'Email: {email}')
print('Contraseña: [OCULTA]')
"""
        
        # Ejecutar el código Django
        resultado = subprocess.run([
            sys.executable, "manage.py", "shell"
        ], input=django_code, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print("✅ Proceso de creación de superusuario completado")
            if resultado.stdout.strip():
                lines = resultado.stdout.strip().split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('>>>'):
                        print(f"   {line}")
        else:
            print("❌ Error al crear superusuario:")
            if resultado.stderr:
                print(f"   {resultado.stderr.strip()}")
            return False
        
        # Información final
        print(f"\n🎉 ¡SUPERUSUARIO CONFIGURADO!")
        print("="*40)
        print(f"🌐 Para acceder al admin de Django:")
        print("   1. Ejecuta: python manage.py runserver")
        print("   2. Ve a: http://localhost:8000/admin/")
        print(f"   3. Usuario: {username}")
        print("   4. Contraseña: [la que configuraste]")
        
        return True
        
    except FileNotFoundError:
        print("❌ Error: No se encontró manage.py en el directorio actual")
        print("   Asegúrate de ejecutar este script desde la raíz del proyecto Django")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def aplicar_migraciones_y_superusuario():
    """Aplica migraciones a la base de datos y crea un superusuario"""
    print("\n🚀 APLICANDO MIGRACIONES Y CREANDO SUPERUSUARIO")
    print("-" * 50)
    
    try:
        # Paso 1: Generar migraciones
        print("📝 Paso 1: Generando migraciones...")
        resultado = subprocess.run([
            sys.executable, "manage.py", "makemigrations"
        ], capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print("✅ Migraciones generadas exitosamente")
            if resultado.stdout.strip():
                print(f"   📄 {resultado.stdout.strip()}")
        else:
            print("⚠️  Advertencia al generar migraciones:")
            if resultado.stderr:
                print(f"   {resultado.stderr.strip()}")
        
        # Paso 2: Aplicar migraciones
        print("\n🔄 Paso 2: Aplicando migraciones a la base de datos...")
        resultado = subprocess.run([
            sys.executable, "manage.py", "migrate"
        ], capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print("✅ Migraciones aplicadas exitosamente")
            if resultado.stdout.strip():
                # Mostrar solo las líneas importantes
                lines = resultado.stdout.strip().split('\n')
                for line in lines:
                    if 'Applying' in line or 'OK' in line:
                        print(f"   {line}")
        else:
            print("❌ Error al aplicar migraciones:")
            if resultado.stderr:
                print(f"   {resultado.stderr.strip()}")
            return False
        
        # Paso 3: Crear superusuario
        print("\n👤 Paso 3: Configuración del superusuario")
        print("¿Cómo quieres crear el superusuario?")
        print("   1. Modo rápido (usuario: architin777, contraseña: architin777)")
        print("   2. Personalizado (elegir usuario y contraseña)")
        
        while True:
            opcion = input("\n🔢 Elige una opción (1-2): ").strip()
            
            if opcion == "1":
                # Modo rápido
                username = "architin777"
                password = "architin777"
                email = "admin@example.com"
                print(f"\n⚡ Creando superusuario rápido: {username}")
                break
                
            elif opcion == "2":
                # Modo personalizado
                print("\n✏️  Configuración personalizada:")
                username = input("   👤 Nombre de usuario: ").strip()
                if not username:
                    print("❌ El nombre de usuario no puede estar vacío")
                    continue
                
                email = input("   📧 Email (opcional, presiona Enter para usar admin@example.com): ").strip()
                if not email:
                    email = "admin@example.com"
                
                import getpass
                password = getpass.getpass("   🔒 Contraseña: ")
                if not password:
                    print("❌ La contraseña no puede estar vacía")
                    continue
                
                confirm_password = getpass.getpass("   🔒 Confirmar contraseña: ")
                if password != confirm_password:
                    print("❌ Las contraseñas no coinciden")
                    continue
                
                print(f"\n👤 Creando superusuario: {username}")
                break
            else:
                print("❌ Opción no válida. Elige 1 o 2")
        
        # Crear el superusuario usando Django shell
        django_code = f"""
from django.contrib.auth import get_user_model
User = get_user_model()

# Verificar si el usuario ya existe
if User.objects.filter(username='{username}').exists():
    print('⚠️  El usuario {username} ya existe')
    user = User.objects.get(username='{username}')
    user.set_password('{password}')
    user.save()
    print('🔄 Contraseña actualizada')
else:
    user = User.objects.create_superuser(
        username='{username}',
        email='{email}',
        password='{password}'
    )
    print('✅ Superusuario creado exitosamente')

print(f'👤 Usuario: {username}')
print(f'📧 Email: {email}')
print('🔑 Contraseña: [OCULTA]')
"""
        
        # Ejecutar el código Django
        resultado = subprocess.run([
            sys.executable, "manage.py", "shell"
        ], input=django_code, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print("✅ Proceso de creación de superusuario completado")
            if resultado.stdout.strip():
                lines = resultado.stdout.strip().split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('>>>'):
                        print(f"   {line}")
        else:
            print("❌ Error al crear superusuario:")
            if resultado.stderr:
                print(f"   {resultado.stderr.strip()}")
            return False
        
        # Resumen final
        print(f"\n🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!")
        print("="*50)
        print("✅ Migraciones aplicadas")
        print("✅ Superusuario configurado")
        print(f"\n🌐 Para acceder al admin de Django:")
        print("   1. Ejecuta: python manage.py runserver")
        print("   2. Ve a: http://localhost:8000/admin/")
        print(f"   3. Usuario: {username}")
        print("   4. Contraseña: [la que configuraste]")
        
        return True
        
    except FileNotFoundError:
        print("❌ Error: No se encontró manage.py en el directorio actual")
        print("   Asegúrate de ejecutar este script desde la raíz del proyecto Django")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def main():
    """Función principal que ejecuta el menú interactivo"""
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\n🔢 Selecciona una opción (0-8): ").strip()
            
            if opcion == "0":
                print("\n👋 ¡Hasta luego!")
                break
                
            elif opcion == "1":
                limpiar_migraciones()
                
            elif opcion == "2":
                database_url = os.getenv("DATABASE_URL", "")
                if database_url.startswith("postgres"):
                    vaciar_base_datos_supabase()
                else:
                    print("\n❌ No se detectó una base de datos PostgreSQL/Supabase")
                    print("   Verifica tu configuración DATABASE_URL")
                    
            elif opcion == "3":
                database_url = os.getenv("DATABASE_URL", "")
                if database_url and not database_url.startswith("postgres"):
                    borrar_sqlite_local()
                else:
                    print("\n❌ No se detectó una base de datos SQLite")
                    print("   Verifica tu configuración DATABASE_URL")
                    
            elif opcion == "4":
                limpieza_completa()
                
            elif opcion == "5":
                mostrar_informacion()
                
            elif opcion == "6":
                database_url = os.getenv("DATABASE_URL", "")
                if database_url.startswith("postgres"):
                    reparar_conflictos_django()
                else:
                    print("\n❌ Esta opción solo funciona con PostgreSQL/Supabase")
                    print("   Verifica tu configuración DATABASE_URL")
                
            elif opcion == "7":
                aplicar_migraciones_y_superusuario()
                
            elif opcion == "8":
                crear_superusuario()
                
            else:
                print("\n❌ Opción no válida. Por favor, elige entre 0-8")
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Operación interrumpida por el usuario")
            print("👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            
        # Pausa antes de mostrar el menú nuevamente
        if opcion != "0":
            input("\n⏸️  Presiona Enter para continuar...")


if __name__ == "__main__":
    main()