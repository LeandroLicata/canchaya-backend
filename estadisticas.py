# estadisticas.py — Cálculo de métricas sobre las reservas y generación de gráficos.
# [GUS] Gustavo Di Paola.
#
# ESQUELETO: las firmas son las acordadas en CONTRATO_MODULOS.md y main.py ya las usa.
# Cada función devuelve un valor neutro hasta que Gustavo la implemente.
#
# graficar_ocupacion() es el eje de investigación del proyecto (matplotlib) y es la
# única función que necesita una biblioteca externa: importala adentro de la función,
# para que el resto del programa funcione aunque matplotlib no esté instalado.


def ocupacion_por_horario(lista_reservas):
    """Cuenta cuántas reservas confirmadas hay en cada franja horaria.

    Parámetros:
        lista_reservas: lista de reservas a analizar.
    Devuelve:
        Diccionario {"18:00": 4, "19:00": 7, ...} con todas las horas de HORARIOS.
    """
    # TODO [GUS]: arrancar el diccionario en 0 para cada hora de estructuras.HORARIOS
    # y recorrer las reservas confirmadas sumando de a uno.
    return {}


def ingresos_por_complejo(lista_reservas, lista_complejos):
    """Calcula cuánto facturó cada complejo con las reservas confirmadas.

    Parámetros:
        lista_reservas: lista de reservas a analizar.
        lista_complejos: para obtener el precio por hora y el nombre.
    Devuelve:
        Diccionario {"Estadio 5": 54000, ...}.
    """
    # TODO [GUS]: cada reserva confirmada suma el precio_hora de su complejo.
    return {}


def ranking_complejos(lista_reservas, lista_complejos, tope=3):
    """Arma el ranking de los complejos con más reservas.

    Parámetros:
        lista_reservas: lista de reservas a analizar.
        lista_complejos: para obtener los nombres.
        tope: cuántos complejos devolver (por defecto 3).
    Devuelve:
        Lista de tuplas (nombre, cantidad) ordenada de mayor a menor.
    """
    # TODO [GUS]: contar por complejo, ordenar con utils.ordenar_por() y recortar al tope.
    return []


def porcentaje_cancelaciones(lista_reservas):
    """Calcula qué porcentaje de las reservas terminó cancelado.

    Parámetros:
        lista_reservas: lista de reservas a analizar.
    Devuelve:
        Número con un decimal. 0.0 si todavía no hay reservas.
    """
    # TODO [GUS]: cuidado con la división por cero cuando la lista está vacía.
    return 0.0


def graficar_ocupacion(ocupacion, ruta):
    """Genera un gráfico de barras de la ocupación por horario y lo guarda como PNG.

    Parámetros:
        ocupacion: diccionario devuelto por ocupacion_por_horario().
        ruta: ruta del archivo PNG a generar.
    Devuelve:
        True si pudo generar el gráfico, False si no.
    """
    # TODO [GUS]: import matplotlib.pyplot adentro de la función y dentro de un
    # try/except ImportError, para que el programa siga andando sin la biblioteca.
    # Crear la carpeta destino si no existe.
    return False
