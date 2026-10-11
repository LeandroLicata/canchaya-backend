# tests/test_utils.py — Pruebas de las validaciones de utils.py que usa la API.
# [LEA] Leandro Licata.

import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils

COMPLEJOS = [{"id": 1, "nombre": "Estadio 5"}, {"id": 2, "nombre": "La Redonda"}]


def datos_validos():
    """Arma una reserva válida para mañana, que cada prueba modifica en un campo.

    Devuelve:
        Diccionario con los campos que recibe validar_reserva().
    """
    manana = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    return {
        "nombre_cliente": "Lionel Perez",
        "email": "lionel@ejemplo.com",
        "telefono": "261 123 4567",
        "id_complejo": 1,
        "fecha": manana,
        "hora": "20:00",
        "jugadores": 10,
        "comentarios": "",
    }


def test_buscar_complejo():
    """Encuentra un complejo por id y devuelve None si no existe."""
    assert utils.buscar_complejo(COMPLEJOS, 2)["nombre"] == "La Redonda"
    assert utils.buscar_complejo(COMPLEJOS, 99) is None


def test_reserva_valida():
    """Una reserva con todos los campos correctos no tiene errores."""
    assert utils.validar_reserva(datos_validos(), COMPLEJOS) is None


def test_comentarios_son_opcionales():
    """Si no vienen comentarios, la reserva igual es válida."""
    datos = datos_validos()
    del datos["comentarios"]
    assert utils.validar_reserva(datos, COMPLEJOS) is None


def test_campos_invalidos():
    """Cada campo con un valor o tipo incorrecto devuelve un mensaje de error."""
    casos = [
        ("nombre_cliente", "  Li "),
        ("email", "lionel@ejemplo"),
        ("telefono", 2611234567),
        ("id_complejo", 99),
        ("id_complejo", "1"),
        ("fecha", "2020-01-01"),
        ("fecha", "2026-02-30"),
        ("hora", "17:00"),
        ("jugadores", 1),
        ("jugadores", "10"),
        ("jugadores", True),
        ("comentarios", None),
    ]
    for campo, valor in casos:
        datos = datos_validos()
        datos[campo] = valor
        assert utils.validar_reserva(datos, COMPLEJOS) is not None, (campo, valor)


def test_campo_faltante_y_formato_invalido():
    """Falta un campo obligatorio, o los datos no son un diccionario."""
    datos = datos_validos()
    del datos["email"]
    assert utils.validar_reserva(datos, COMPLEJOS) is not None
    assert utils.validar_reserva(["no", "es", "dict"], COMPLEJOS) is not None
