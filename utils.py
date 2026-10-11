# utils.py — Funciones auxiliares: validaciones de entrada, búsquedas,
# ordenamiento y formateo para pantalla.
# [GUS] Gustavo Di Paola.
#
# Las firmas son las acordadas en CONTRATO_MODULOS.md.
# SUPUESTO: cada reserva es un dict con las claves
#   id, nombre_cliente, email, telefono, id_complejo, fecha (AAAA-MM-DD), hora,
#   jugadores, estado
# y cada complejo un dict con las claves id y nombre.
# Si el contrato usa otros nombres, cambiarlos solo en formatear_reserva y fila_csv.

from datetime import datetime, date

import estructuras


def pedir_texto(mensaje, largo_minimo=3):
    """Pide un texto por teclado y reintenta hasta que sea válido.

    Parámetros:
        mensaje: texto del prompt.
        largo_minimo: cantidad mínima de caracteres (0 permite dejarlo vacío).
    Devuelve:
        El texto ingresado, sin espacios al principio ni al final.
    """
    while True:
        texto = input(mensaje).strip()
        if len(texto) >= largo_minimo:
            return texto
        print(f"Error: debe tener al menos {largo_minimo} caracteres.")


def pedir_entero(mensaje, minimo, maximo):
    """Pide un número entero dentro de un rango y reintenta hasta lograrlo.

    Parámetros:
        mensaje: texto del prompt.
        minimo y maximo: límites aceptados, ambos incluidos.
    Devuelve:
        El número ingresado.
    """
    while True:
        try:
            numero = int(input(mensaje))
        except ValueError:
            print("Error: ingresá un número entero.")
            continue
        if minimo <= numero <= maximo:
            return numero
        print(f"Error: el número debe estar entre {minimo} y {maximo}.")


def pedir_opcion(mensaje, opciones):
    """Pide una opción de una lista y reintenta hasta que sea una válida.

    Parámetros:
        mensaje: texto del prompt.
        opciones: lista de valores aceptados (textos o números).
    Devuelve:
        El elemento elegido, del mismo tipo que venía en la lista.
    """
    while True:
        ingreso = input(mensaje).strip()
        for opcion in opciones:
            if str(opcion) == ingreso:
                return opcion
        validas = ", ".join(str(o) for o in opciones)
        print(f"Error: opción inválida. Elegí una de: {validas}.")


def validar_email(texto):
    """Indica si un email tiene un formato aceptable.

    Parámetros:
        texto: la dirección a revisar.
    Devuelve:
        True si es válida, False si no.
    """
    if " " in texto or texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    if usuario == "" or dominio == "" or "." not in dominio:
        return False
    if dominio.startswith(".") or dominio.endswith("."):
        return False
    return True


def validar_fecha(texto):
    """Indica si una fecha tiene formato AAAA-MM-DD y existe en el calendario.

    Se usa en las búsquedas, donde las fechas pasadas son válidas.

    Parámetros:
        texto: la fecha a revisar.
    Devuelve:
        True si es válida, False si no.
    """
    # strptime acepta "2026-9-5"; el largo 10 obliga a escribir ceros.
    if len(texto) != 10:
        return False
    try:
        datetime.strptime(texto, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def validar_fecha_reserva(texto):
    """Indica si una fecha sirve para reservar: válida y no anterior a hoy.

    Parámetros:
        texto: la fecha a revisar.
    Devuelve:
        True si es válida y futura (o de hoy), False si no.
    """
    if not validar_fecha(texto):
        return False
    fecha = datetime.strptime(texto, "%Y-%m-%d").date()
    return fecha >= date.today()


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
    encontradas = []
    for reserva in lista_reservas:
        if campo not in reserva:
            continue
        actual = reserva[campo]
        if isinstance(valor, str) and isinstance(actual, str):
            coincide = valor.lower() in actual.lower()
        else:
            coincide = actual == valor
        if coincide:
            encontradas.append(reserva)
    return encontradas


def ordenar_por(lista, campo, descendente=False):
    """Ordena una lista de diccionarios por uno de sus campos.

    Parámetros:
        lista: lista de diccionarios a ordenar.
        campo: clave por la que se ordena.
        descendente: True para ordenar de mayor a menor.
    Devuelve:
        Una lista nueva, ordenada. No modifica la original.
    """
    resultado = list(lista)  # copia: la original queda intacta
    for i in range(1, len(resultado)):
        actual = resultado[i]
        j = i - 1
        while j >= 0:
            if descendente:
                debe_moverse = resultado[j][campo] < actual[campo]
            else:
                debe_moverse = resultado[j][campo] > actual[campo]
            if not debe_moverse:
                break
            resultado[j + 1] = resultado[j]
            j -= 1
        resultado[j + 1] = actual
    return resultado


# [LEA] Agregada para la API: hace falta saber si un id de complejo existe.
def buscar_complejo(lista_complejos, id_complejo):
    """Busca un complejo por su id.

    Parámetros:
        lista_complejos: lista donde buscar.
        id_complejo: id del complejo buscado.
    Devuelve:
        El diccionario del complejo, o None si no existe.
    """
    for complejo in lista_complejos:
        if complejo["id"] == id_complejo:
            return complejo
    return None


def _nombre_complejo(id_complejo, lista_complejos):
    """Devuelve el nombre del complejo, o '?' si no se encuentra el id."""
    complejo = buscar_complejo(lista_complejos, id_complejo)
    if complejo is None:
        return "?"
    return complejo["nombre"]


def formatear_reserva(reserva, lista_complejos):
    """Arma una línea de texto legible con los datos de una reserva.

    Parámetros:
        reserva: el diccionario a mostrar.
        lista_complejos: para reemplazar el id del complejo por su nombre.
    Devuelve:
        Una cadena de una sola línea, lista para imprimir.
    """
    nombre = _nombre_complejo(reserva["id_complejo"], lista_complejos)
    anio, mes, dia = reserva["fecha"].split("-")
    return (f"#{reserva['id']} {dia}/{mes} {reserva['hora']} — {nombre} — "
            f"{reserva['nombre_cliente']} ({reserva['estado']})")


def fila_csv(reserva, lista_complejos):
    """Convierte una reserva en la fila que se escribe en el reporte CSV.

    Parámetros:
        reserva: el diccionario a exportar.
        lista_complejos: para escribir el nombre del complejo en vez del id.
    Devuelve:
        Lista de valores en el orden de los encabezados definidos en main.py:
        id, cliente, email, telefono, complejo, hora, jugadores, estado.
    """
    nombre = _nombre_complejo(reserva["id_complejo"], lista_complejos)
    return [
        reserva["id"],
        reserva["nombre_cliente"],
        reserva["email"],
        reserva["telefono"],
        nombre,
        reserva["hora"],
        reserva["jugadores"],
        reserva["estado"],
    ]


# [LEA] Agregadas para la API: en consola cada dato se valida al pedirlo, pero la API
# recibe la reserva completa en un JSON y tiene que validarla de una sola vez.
def es_texto_valido(valor, largo_minimo):
    """Indica si un valor es un texto con al menos cierta cantidad de caracteres.

    Parámetros:
        valor: el dato a revisar (puede venir de cualquier tipo desde el JSON).
        largo_minimo: cantidad mínima de caracteres, sin contar espacios de los bordes.
    Devuelve:
        True si es un texto suficientemente largo, False si no.
    """
    return isinstance(valor, str) and len(valor.strip()) >= largo_minimo


def es_entero_en_rango(valor, minimo, maximo):
    """Indica si un valor es un número entero dentro de un rango.

    Parámetros:
        valor: el dato a revisar.
        minimo y maximo: límites aceptados, ambos incluidos.
    Devuelve:
        True si es un entero entre minimo y maximo, False si no.
    """
    # bool es subclase de int en Python: se descarta para que True no cuente como 1.
    if not isinstance(valor, int) or isinstance(valor, bool):
        return False
    return minimo <= valor <= maximo


def validar_reserva(datos, lista_complejos):
    """Valida todos los campos de una reserva nueva recibida de una sola vez.

    Parámetros:
        datos: diccionario con los campos que recibe estructuras.crear_reserva().
        lista_complejos: para verificar que el complejo elegido exista.
    Devuelve:
        None si todo es válido, o un texto con el primer error encontrado.
    """
    if not isinstance(datos, dict):
        return "Los datos de la reserva tienen un formato inválido."
    if not es_texto_valido(datos.get("nombre_cliente"), 3):
        return "El nombre debe tener al menos 3 caracteres."
    email = datos.get("email")
    if not isinstance(email, str) or not validar_email(email):
        return "El email no es válido."
    if not es_texto_valido(datos.get("telefono"), 6):
        return "El teléfono debe tener al menos 6 caracteres."
    if buscar_complejo(lista_complejos, datos.get("id_complejo")) is None:
        return "El complejo elegido no existe."
    fecha = datos.get("fecha")
    if not isinstance(fecha, str) or not validar_fecha_reserva(fecha):
        return "La fecha no es válida o ya pasó (formato AAAA-MM-DD)."
    if datos.get("hora") not in estructuras.HORARIOS:
        return "El horario no es válido."
    if not es_entero_en_rango(datos.get("jugadores"), estructuras.MIN_JUGADORES,
                              estructuras.MAX_JUGADORES):
        return "La cantidad de jugadores debe estar entre {0} y {1}.".format(
            estructuras.MIN_JUGADORES, estructuras.MAX_JUGADORES)
    if not isinstance(datos.get("comentarios", ""), str):
        return "Los comentarios deben ser texto."
    return None
