# utils.py — Funciones auxiliares: validaciones de entrada, búsquedas,
# ordenamiento y formateo para pantalla.
# [GUS] Gustavo Di Paola.
#
# ESQUELETO: las firmas son las acordadas en CONTRATO_MODULOS.md y main.py ya las usa.
#
# OJO con los valores neutros de este módulo: main.py reintenta la carga de un dato
# hasta que el validador lo acepta, así que un validador que devuelva siempre False
# deja el programa en un bucle infinito. Por eso los stubs devuelven el valor que
# corta el bucle (True / "0"); al implementarlos hay que reemplazarlos.


def pedir_texto(mensaje, largo_minimo=3):
    """Pide un texto por teclado y reintenta hasta que sea válido.

    Parámetros:
        mensaje: texto del prompt.
        largo_minimo: cantidad mínima de caracteres (0 permite dejarlo vacío).
    Devuelve:
        El texto ingresado, sin espacios al principio ni al final.
    """
    # TODO [GUS]: bucle while con input(), .strip() y mensaje de error claro.
    return ""


def pedir_entero(mensaje, minimo, maximo):
    """Pide un número entero dentro de un rango y reintenta hasta lograrlo.

    Parámetros:
        mensaje: texto del prompt.
        minimo y maximo: límites aceptados, ambos incluidos.
    Devuelve:
        El número ingresado.
    """
    # TODO [GUS]: int(input()) dentro de try/except ValueError, más la
    # comprobación del rango.
    return minimo


def pedir_opcion(mensaje, opciones):
    """Pide una opción de una lista y reintenta hasta que sea una válida.

    Parámetros:
        mensaje: texto del prompt.
        opciones: lista de valores aceptados (textos o números).
    Devuelve:
        El elemento elegido, del mismo tipo que venía en la lista.
    """
    # TODO [GUS]: comparar como texto para que sirva igual con ids numéricos,
    # y devolver el elemento original de la lista.
    # Devuelve "0" para que el menú de main.py termine mientras sea un stub.
    return "0"


def validar_email(texto):
    """Indica si un email tiene un formato aceptable.

    Parámetros:
        texto: la dirección a revisar.
    Devuelve:
        True si es válida, False si no.
    """
    # TODO [GUS]: exigir un solo "@", algo antes y después, y un "." en el dominio.
    return True


def validar_fecha(texto):
    """Indica si una fecha tiene formato AAAA-MM-DD y existe en el calendario.

    Se usa en las búsquedas, donde las fechas pasadas son válidas.

    Parámetros:
        texto: la fecha a revisar.
    Devuelve:
        True si es válida, False si no.
    """
    # TODO [GUS]: datetime.strptime(texto, "%Y-%m-%d") dentro de try/except ValueError.
    return True


def validar_fecha_reserva(texto):
    """Indica si una fecha sirve para reservar: válida y no anterior a hoy.

    Parámetros:
        texto: la fecha a revisar.
    Devuelve:
        True si es válida y futura (o de hoy), False si no.
    """
    # TODO [GUS]: reutilizar validar_fecha() y después comparar contra date.today().
    return True


def buscar_reservas(lista_reservas, campo, valor):
    """Filtra las reservas cuyo campo coincide con el valor buscado.

    Parámetros:
        lista_reservas: lista donde buscar.
        campo: clave del diccionario a comparar.
        valor: valor buscado; en textos la coincidencia es parcial y sin distinguir
            mayúsculas.
    Devuelve:
        Lista con las reservas encontradas (vacía si no hay ninguna).
    """
    # TODO [GUS]: recorrer la lista y comparar segun el tipo del valor.
    return []


def ordenar_por(lista, campo, descendente=False):
    """Ordena una lista de diccionarios por uno de sus campos.

    Parámetros:
        lista: lista de diccionarios a ordenar.
        campo: clave por la que se ordena.
        descendente: True para ordenar de mayor a menor.
    Devuelve:
        Una lista nueva, ordenada. No modifica la original.
    """
    # TODO [GUS]: algoritmo de inserción escrito a mano, no sorted().
    # La consigna valora el algoritmo propio.
    return lista


def formatear_reserva(reserva, lista_complejos):
    """Arma una línea de texto legible con los datos de una reserva.

    Parámetros:
        reserva: el diccionario a mostrar.
        lista_complejos: para reemplazar el id del complejo por su nombre.
    Devuelve:
        Una cadena de una sola línea, lista para imprimir.
    """
    # TODO [GUS]: por ejemplo "#3 25/09 20:00 — Estadio 5 — Lionel Pérez (confirmada)".
    return ""


def fila_csv(reserva, lista_complejos):
    """Convierte una reserva en la fila que se escribe en el reporte CSV.

    Parámetros:
        reserva: el diccionario a exportar.
        lista_complejos: para escribir el nombre del complejo en vez del id.
    Devuelve:
        Lista de valores en el orden de los encabezados definidos en main.py:
        id, cliente, email, telefono, complejo, hora, jugadores, estado.
    """
    # TODO [GUS]: devolver los valores en ese orden exacto.
    return []
