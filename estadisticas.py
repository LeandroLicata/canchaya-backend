# estadisticas.py — Cálculo de métricas sobre las reservas y generación de gráficos.
# [GUS] Gustavo Di Paola.
#
# graficar_barras() es el eje de investigación del proyecto (matplotlib) y es la
# única función que necesita una biblioteca externa: se importa adentro de la función,
# para que el resto del programa funcione aunque matplotlib no esté instalado.
# graficar_ocupacion() y graficar_ingresos() la reutilizan para no repetir código.

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
        complejo = utils.buscar_complejo(lista_complejos, reserva["id_complejo"])
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


def graficar_barras(datos, titulo, etiqueta_x, etiqueta_y, ruta):
    """Genera un gráfico de barras genérico y lo guarda como PNG.

    Es la parte común de matplotlib: la usan todos los gráficos del módulo.

    Parámetros:
        datos: diccionario {etiqueta: valor}.
        titulo: título del gráfico.
        etiqueta_x: texto del eje horizontal.
        etiqueta_y: texto del eje vertical.
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

    if not datos:
        return False

    try:
        carpeta = os.path.dirname(ruta)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)

        plt.figure(figsize=(9, 5))
        plt.bar(list(datos.keys()), list(datos.values()), color="#2e86de")
        plt.title(titulo)
        plt.xlabel(etiqueta_x)
        plt.ylabel(etiqueta_y)
        plt.tight_layout()
        plt.savefig(ruta)
        return True
    except OSError:
        return False
    finally:
        plt.close()


def graficar_ocupacion(ocupacion, ruta):
    """Genera el gráfico de ocupación por horario.

    Parámetros:
        ocupacion: diccionario devuelto por ocupacion_por_horario().
        ruta: ruta del archivo PNG a generar.
    Devuelve:
        True si pudo generar el gráfico, False si no.
    """
    return graficar_barras(ocupacion,
                           "Ocupación por horario (reservas confirmadas)",
                           "Horario", "Cantidad de reservas", ruta)


def graficar_ingresos(ingresos, ruta):
    """Genera el gráfico de ingresos por complejo.

    Parámetros:
        ingresos: diccionario devuelto por ingresos_por_complejo().
        ruta: ruta del archivo PNG a generar.
    Devuelve:
        True si pudo generar el gráfico, False si no.
    """
    return graficar_barras(ingresos, "Ingresos por complejo (confirmadas)",
                           "Complejo", "Ingresos ($)", ruta)
