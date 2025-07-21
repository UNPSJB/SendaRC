from django.test import TestCase
from servicio.models import TipoServicio, Empleado
from servicio.views import calcularImportePresupuesto

class CalculoImportePresupuestoTest(TestCase):
    def test_importe_sugerido(self):
        # Preparar los mocks
        class TipoServicioMock:
            def __init__(self, nombre, precio_unitario):
                self.nombre = nombre
                self.precio_unitario = precio_unitario

            def getPrecio(self, cantidad):
                return self.precio_unitario * cantidad

        class EmpleadoMock:
            @staticmethod
            def getSueldoBasico():
                return 240000  # sueldo mensual

        # Parchar manualmente
        import servicio.views
        servicio.views.Empleado = EmpleadoMock

        listaTipoServicio = [
            {"tipo_servicio": TipoServicioMock("Limpieza", 100), "cantidad": 2},
            {"tipo_servicio": TipoServicioMock("Desinfección", 150), "cantidad": 1}
        ]
        cantEmpleados = 2
        cantFrecuencias = 3
        tipo = 2

        resultado = calcularImportePresupuesto(listaTipoServicio, cantEmpleados, cantFrecuencias, tipo)

        self.assertEqual(resultado["total_servicios"], 1050)
        self.assertEqual(resultado["porcentaje_ganancia"], 157.5)
        self.assertEqual(resultado["mano_obra_servicio"], 240000)
        self.assertEqual(resultado["importe_sugerido"], 241207.5)
