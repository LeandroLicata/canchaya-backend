# estadisticas.py — Cálculo de métricas sobre las reservas y generación de gráficos.
# [GUS] Gustavo Di Paola.
#
# graficar_ocupacion() es el eje de investigación del proyecto (matplotlib) y es la
# única función que necesita una biblioteca externa: se importa adentro de la función,
# para que el resto del programa funcione aunque matplotlib no esté instalado.

import os

import estructuras
import utils


def ocupacion_por_horario(lista_reservas):
    """Cuenta cuántas reservas confirmadas hay en cada franja horaria.

    Parámetros:
        lista_reservas: lista de reservas a analizar.
    Devuelve:
        Diccionario {"18:00": 4, "19:00": 7, ...} con todas las horas de HORARIOS.
    """
    ocupacion = {}
    for hora in estructuras.HORARIOS:
        ocupacion[hora] = 0

    for reserva in lista_reservas:
        if (reserva["estado"] == estructuras.ESTADO_CONFIRMADA
                and reserva["hora"] in ocupacion):
            ocupacion[reserva["hora"]] += 1
    return ocupacion


def buscar_complejo_por_id(lista_complejos, id_complejo):
    """Busca un complejo por su id.

    Parámetros:
        lista_complejos: lista de complejos.
        id_complejo: id a buscar.
    Devuelve:
        El diccionario del complejo, o None si no existe.
    """
    for complejo in lista_complejos:
        if complejo["id"] == id_complejo:
            return complejo
    return None


def ingresos_por_complejo(lista_reservas, lista_complejos):
    """Calcula cuánto facturó cada complejo con las reservas confirmadas.

    Parámetros:
        lista_reservas: lista de reservas a analizar.
        lista_complejos: para obtener el precio por hora y el nombre.
    Devuelve:
        Diccionario {"Estadio 5": 54000, ...}.
    """
    ingresos = {}
    for complejo in lista_complejos:
        ingresos[complejo["nombre"]] = 0

    for reserva in lista_reservas:
        if reserva["estado"] != estructuras.ESTADO_CONFIRMADA:
            continue
        complejo = buscar_complejo_por_id(lista_complejos, reserva["id_complejo"])
        if complejo is not None:
            ingresos[complejo["nombre"]] += complejo["precio_hora"]
    return ingresos


def ranking_complejos(lista_reservas, lista_complejos, tope=3):
    """Arma el ranking de los complejos con más reservas confirmadas.

    Parámetros:
        lista_reservas: lista de reservas a analizar.
        lista_complejos: para obtener los nombres.
        tope: cuántos complejos devolver (por defecto 3).
    Devuelve:
        Lista de tuplas (nombre, cantidad) ordenada de mayor a menor.
    """
    conteo = []
    for complejo in lista_complejos:
        cantidad = 0
        for reserva in lista_reservas:
            if (reserva["id_complejo"] == complejo["id"]
                    and reserva["estado"] == estructuras.ESTADO_CONFIRMADA):
                cantidad += 1
        conteo.append({"nombre": complejo["nombre"], "cantidad": cantidad})

    ordenado = utils.ordenar_por(conteo, "cantidad", True)

    ranking = []
    for item in ordenado[:tope]:
        ranking.append((item["nombre"], item["cantidad"]))
    return ranking


def porcentaje_cancelaciones(lista_reservas):
    """Calcula qué porcentaje de las reservas terminó cancelado.

    Parámetros:
        lista_reservas: lista de reservas a analizar.
    Devuelve:
        Número con un decimal. 0.0 si todavía no hay reservas.
    """
    total = len(lista_reservas)
    if total == 0:
        return 0.0

    canceladas = 0
    for reserva in lista_reservas:
        if reserva["estado"] == estructuras.ESTADO_CANCELADA:
            canceladas += 1
    return round(canceladas * 100 / total, 1)


def graficar_ocupacion(ocupacion, ruta):
    """Genera un gráfico de barras de la ocupación por horario y lo guarda como PNG.

    Parámetros:
        ocupacion: diccionario devuelto por ocupacion_por_horario().
        ruta: ruta del archivo PNG a generar.
    Devuelve:
        True si pudo generar el gráfico, False si no.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")  # sin ventana: solo guarda el archivo
        import matplotlib.pyplot as plt
    except ImportError:
        return False

    try:
        carpeta = os.path.dirname(ruta)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)

        plt.figure(figsize=(9, 5))
        plt.bar(list(ocupacion.keys()), list(ocupacion.values()), color="#2e86de")
        plt.title("Ocupación por horario (reservas confirmadas)")
        plt.xlabel("Horario")
        plt.ylabel("Cantidad de reservas")
        plt.tight_layout()
        plt.savefig(ruta)
        plt.close()
        return True
    except OSError:
        return False
