# test_estructuras.py — Pruebas unitarias de estructuras.py: alta de reservas,
# disponibilidad, cancelación, modificación y cola FIFO de lista de espera.
# [FED] Federico Cabrera.
#
# Se ejecutan desde la raíz del proyecto con:  python -m unittest discover tests

import unittest

import estructuras


def datos_de_prueba(hora="20:00", id_complejo=1, fecha="2026-10-10"):
    """Arma los datos que cargaría un usuario para una reserva.

    Parámetros:
        hora, id_complejo y fecha del turno (tienen valores por defecto).
    Devuelve:
        Diccionario con los campos que recibe crear_reserva().
    """
    return {
        "nombre_cliente": "Lionel Perez",
        "email": "lionel@ejemplo.com",
        "telefono": "261 123 4567",
        "id_complejo": id_complejo,
        "fecha": fecha,
        "hora": hora,
        "jugadores": 10,
        "comentarios": "",
    }


def reservar(lista_reservas, hora="20:00"):
    """Crea y agrega una reserva en un paso, para no repetirlo en cada prueba.

    Parámetros:
        lista_reservas y hora del turno.
    Devuelve:
        Tupla (reserva, estado) con la reserva agregada y el estado que le tocó.
    """
    reserva = estructuras.crear_reserva(lista_reservas, datos_de_prueba(hora))
    lista_reservas, estado = estructuras.agregar_reserva(lista_reservas, reserva)
    return reserva, estado


class TestAltaYDisponibilidad(unittest.TestCase):
    """Alta de reservas, id autoincremental y horarios libres."""

    def test_id_autoincremental(self):
        """El id es el máximo existente + 1, aunque falten ids intermedios."""
        lista = [{"id": 1}, {"id": 5}]
        reserva = estructuras.crear_reserva(lista, datos_de_prueba())
        self.assertEqual(reserva["id"], 6)
        self.assertEqual(estructuras.crear_reserva([], datos_de_prueba())["id"], 1)

    def test_turno_libre_se_confirma_y_ocupado_va_a_espera(self):
        """La primera reserva de un turno se confirma; la segunda queda en espera."""
        lista = []
        _, estado_1 = reservar(lista)
        _, estado_2 = reservar(lista)
        self.assertEqual(estado_1, estructuras.ESTADO_CONFIRMADA)
        self.assertEqual(estado_2, estructuras.ESTADO_EN_ESPERA)
        self.assertEqual(len(lista), 2)

    def test_horarios_disponibles(self):
        """Un turno confirmado desaparece de los horarios libres; uno en espera no."""
        lista = []
        reservar(lista, "20:00")
        reservar(lista, "20:00")
        libres = estructuras.horarios_disponibles(lista, 1, "2026-10-10")
        self.assertEqual(libres, ["18:00", "19:00", "21:00", "22:00"])
        otro_dia = estructuras.horarios_disponibles(lista, 1, "2026-10-11")
        self.assertEqual(otro_dia, list(estructuras.HORARIOS))


class TestCancelarYModificar(unittest.TestCase):
    """Cancelación con motivo y modificación de campos editables."""

    def test_cancelar_libera_el_turno(self):
        """Al cancelar, el estado cambia, se guarda el motivo y el turno queda libre."""
        lista = []
        reserva, _ = reservar(lista)
        lista, cancelada = estructuras.cancelar_reserva(lista, reserva["id"], " Lluvia ")
        self.assertTrue(cancelada)
        self.assertEqual(reserva["estado"], estructuras.ESTADO_CANCELADA)
        self.assertEqual(reserva["motivo_cancelacion"], "Lluvia")
        self.assertFalse(estructuras.esta_ocupado(lista, 1, "2026-10-10", "20:00"))

    def test_cancelar_inexistente_o_repetida(self):
        """No se puede cancelar un id que no existe ni una reserva ya cancelada."""
        lista = []
        reserva, _ = reservar(lista)
        self.assertFalse(estructuras.cancelar_reserva(lista, 99, "x")[1])
        estructuras.cancelar_reserva(lista, reserva["id"], "Lluvia")
        self.assertFalse(estructuras.cancelar_reserva(lista, reserva["id"], "x")[1])

    def test_modificar_solo_campos_editables(self):
        """Se modifican jugadores y comentarios; el horario y los tipos inválidos no."""
        lista = []
        reserva, _ = reservar(lista)
        modificar = estructuras.modificar_reserva
        id_reserva = reserva["id"]
        self.assertTrue(modificar(lista, id_reserva, "jugadores", 8)[1])
        self.assertEqual(reserva["jugadores"], 8)
        self.assertFalse(modificar(lista, id_reserva, "hora", "18:00")[1])
        self.assertFalse(modificar(lista, id_reserva, "jugadores", "8")[1])
        self.assertFalse(modificar(lista, 99, "comentarios", "hola")[1])
        self.assertEqual(reserva["hora"], "20:00")


class TestListaDeEspera(unittest.TestCase):
    """Cola FIFO: el primero en llegar es el primero en ser atendido."""

    def test_siguiente_en_espera_es_fifo(self):
        """Devuelve la reserva en espera más antigua del turno, no la más nueva."""
        lista = []
        reservar(lista)
        primera, _ = reservar(lista)
        segunda, _ = reservar(lista)
        # Se fuerzan las fechas para que el orden no dependa del reloj.
        primera["fecha_registro"] = "2026-09-22 19:00:00"
        segunda["fecha_registro"] = "2026-09-22 18:00:00"
        siguiente = estructuras.siguiente_en_espera(lista, 1, "2026-10-10", "20:00")
        self.assertEqual(siguiente["id"], segunda["id"])

    def test_sin_nadie_en_espera(self):
        """Si no hay reservas en espera para el turno, devuelve None."""
        lista = []
        reservar(lista)
        self.assertIsNone(estructuras.siguiente_en_espera(lista, 1, "2026-10-10", "20:00"))

    def test_confirmar_espera_solo_si_se_libero(self):
        """No se confirma mientras el turno esté ocupado; después de cancelar, sí."""
        lista = []
        titular, _ = reservar(lista)
        en_espera, _ = reservar(lista)
        self.assertFalse(estructuras.confirmar_espera(lista, en_espera["id"])[1])
        estructuras.cancelar_reserva(lista, titular["id"], "No viene")
        self.assertTrue(estructuras.confirmar_espera(lista, en_espera["id"])[1])
        self.assertEqual(en_espera["estado"], estructuras.ESTADO_CONFIRMADA)
        self.assertFalse(estructuras.confirmar_espera(lista, en_espera["id"])[1])


if __name__ == "__main__":
    unittest.main()
