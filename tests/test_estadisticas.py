# test_estadisticas.py — Tests de las métricas y los gráficos de estadisticas.py.
# [GUS] Gustavo Di Paola.

import estadisticas
import estructuras

COMPLEJOS = [
    {"id": 1, "nombre": "Estadio 5", "precio_hora": 18000},
    {"id": 2, "nombre": "La Cancha", "precio_hora": 12000},
]


def armar_reserva(id_complejo, hora, estado=estructuras.ESTADO_CONFIRMADA):
    """Arma una reserva mínima para los tests.

    Parámetros:
        id_complejo: id del complejo reservado.
        hora: horario de la reserva.
        estado: estado de la reserva (confirmada por defecto).
    Devuelve:
        Diccionario con los campos que usan las estadísticas.
    """
    return {"id_complejo": id_complejo, "hora": hora, "estado": estado}


def test_porcentaje_cancelaciones_lista_vacia():
    """Con lista vacía devuelve 0.0 y no falla por división por cero."""
    assert estadisticas.porcentaje_cancelaciones([]) == 0.0


def test_porcentaje_cancelaciones_una_de_cuatro():
    """Una cancelada sobre cuatro reservas da 25.0 por ciento."""
    reservas = [
        armar_reserva(1, "18:00"),
        armar_reserva(1, "19:00"),
        armar_reserva(2, "20:00"),
        armar_reserva(2, "21:00", estructuras.ESTADO_CANCELADA),
    ]
    assert estadisticas.porcentaje_cancelaciones(reservas) == 25.0


def test_ingresos_solo_cuentan_confirmadas():
    """Las canceladas y en espera no suman ingresos."""
    reservas = [
        armar_reserva(1, "18:00"),
        armar_reserva(1, "19:00"),
        armar_reserva(1, "20:00", estructuras.ESTADO_CANCELADA),
        armar_reserva(1, "21:00", estructuras.ESTADO_EN_ESPERA),
    ]
    ingresos = estadisticas.ingresos_por_complejo(reservas, COMPLEJOS)
    assert ingresos["Estadio 5"] == 36000
    assert ingresos["La Cancha"] == 0


def test_ranking_ordenado_de_mayor_a_menor():
    """El ranking pone primero al complejo con más reservas confirmadas."""
    reservas = [
        armar_reserva(2, "18:00"),
        armar_reserva(1, "18:00"),
        armar_reserva(1, "19:00"),
        armar_reserva(1, "20:00"),
    ]
    ranking = estadisticas.ranking_complejos(reservas, COMPLEJOS)
    assert ranking == [("Estadio 5", 3), ("La Cancha", 1)]


def test_ocupacion_incluye_todos_los_horarios():
    """La ocupación tiene todas las horas de HORARIOS, aunque estén en cero."""
    ocupacion = estadisticas.ocupacion_por_horario([armar_reserva(1, "20:00")])
    assert list(ocupacion.keys()) == list(estructuras.HORARIOS)
    assert ocupacion["20:00"] == 1


def test_graficar_barras_sin_datos_devuelve_false(tmp_path):
    """Con datos vacíos no genera el PNG y devuelve False."""
    ruta = str(tmp_path / "vacio.png")
    assert estadisticas.graficar_barras({}, "Titulo", "X", "Y", ruta) is False
