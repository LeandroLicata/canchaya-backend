# estructuras.py — Estructuras de datos del dominio: reservas, disponibilidad
# y la cola FIFO de lista de espera.
# [FED] Federico Cabrera.
#
# Sin clases: las reservas son diccionarios dentro de una lista (lista_reservas).
# Este módulo no imprime nada: calcula y devuelve, y main.py decide qué mostrar.

from datetime import datetime

HORARIOS = ("18:00", "19:00", "20:00", "21:00", "22:00")

ESTADO_CONFIRMADA = "confirmada"
ESTADO_CANCELADA = "cancelada"
ESTADO_EN_ESPERA = "en_espera"

CAMPOS_EDITABLES = ("jugadores", "comentarios")
FORMATO_REGISTRO = "%Y-%m-%d %H:%M:%S"


def crear_reserva(lista_reservas, datos):
    """Arma el diccionario de una reserva nueva.

    Parámetros:
        lista_reservas: lista actual, para calcular el id autoincremental.
        datos: diccionario con los campos que cargó el usuario.
    Devuelve:
        El diccionario de la reserva, con id, fecha_registro y estado inicial.
    """
    # El id es el máximo existente + 1 y no len() + 1: si algún día se borra una
    # reserva de la lista, len() repetiría un id que ya se usó.
    id_maximo = 0
    for reserva in lista_reservas:
        if reserva["id"] > id_maximo:
            id_maximo = reserva["id"]

    return {
        "id": id_maximo + 1,
        "nombre_cliente": datos.get("nombre_cliente", ""),
        "email": datos.get("email", ""),
        "telefono": datos.get("telefono", ""),
        "id_complejo": datos.get("id_complejo"),
        "fecha": datos.get("fecha", ""),
        "hora": datos.get("hora", ""),
        "jugadores": datos.get("jugadores", 0),
        "comentarios": datos.get("comentarios", ""),
        # Estado provisorio: agregar_reserva() lo confirma o lo pasa a en_espera.
        "estado": ESTADO_CONFIRMADA,
        "fecha_registro": datetime.now().strftime(FORMATO_REGISTRO),
        "motivo_cancelacion": "",
    }


def es_del_turno(reserva, id_complejo, fecha, hora):
    """Indica si una reserva corresponde a un turno (complejo, fecha y hora).

    Parámetros:
        reserva: diccionario de la reserva.
        id_complejo, fecha (AAAA-MM-DD) y hora (HH:MM) del turno.
    Devuelve:
        True si los tres campos coinciden, False si no.
    """
    return (reserva["id_complejo"] == id_complejo
            and reserva["fecha"] == fecha
            and reserva["hora"] == hora)


def esta_ocupado(lista_reservas, id_complejo, fecha, hora):
    """Indica si un turno ya está tomado.

    Parámetros:
        lista_reservas, id_complejo, fecha (AAAA-MM-DD) y hora (HH:MM).
    Devuelve:
        True si hay una reserva confirmada para ese turno, False si no.
    """
    for reserva in lista_reservas:
        # Las canceladas y las que están en espera no ocupan la cancha.
        if (reserva["estado"] == ESTADO_CONFIRMADA
                and es_del_turno(reserva, id_complejo, fecha, hora)):
            return True
    return False


def horarios_disponibles(lista_reservas, id_complejo, fecha):
    """Calcula qué horarios quedan libres en un complejo para una fecha.

    Parámetros:
        lista_reservas, id_complejo y fecha (AAAA-MM-DD).
    Devuelve:
        Lista con las horas de HORARIOS que todavía no están ocupadas.
    """
    libres = []
    for hora in HORARIOS:
        if not esta_ocupado(lista_reservas, id_complejo, fecha, hora):
            libres.append(hora)
    return libres


def agregar_reserva(lista_reservas, reserva):
    """Agrega una reserva, confirmada o en lista de espera según haya lugar.

    Parámetros:
        lista_reservas: lista actual.
        reserva: diccionario devuelto por crear_reserva().
    Devuelve:
        Tupla (lista_reservas, estado), con estado "confirmada" o "en_espera".
    """
    if esta_ocupado(lista_reservas, reserva["id_complejo"],
                    reserva["fecha"], reserva["hora"]):
        estado = ESTADO_EN_ESPERA
    else:
        estado = ESTADO_CONFIRMADA
    reserva["estado"] = estado
    lista_reservas.append(reserva)
    return lista_reservas, estado


def cancelar_reserva(lista_reservas, id_reserva, motivo):
    """Marca una reserva como cancelada y guarda el motivo.

    Parámetros:
        lista_reservas, id_reserva y motivo de la cancelación.
    Devuelve:
        Tupla (lista_reservas, True) si la canceló, (lista_reservas, False) si no la encontró.
    """
    # TODO [FED]: buscar por id, cambiar el estado y escribir motivo_cancelacion.
    return lista_reservas, False


def modificar_reserva(lista_reservas, id_reserva, campo, valor):
    """Cambia un campo editable de una reserva.

    Parámetros:
        lista_reservas, id_reserva, campo ("jugadores" o "comentarios") y el valor nuevo.
    Devuelve:
        Tupla (lista_reservas, True) si la modificó, (lista_reservas, False) si no.
    """
    # TODO [FED]: aceptar solo los campos editables; el horario no se cambia acá,
    # se cancela la reserva y se hace una nueva.
    return lista_reservas, False


def siguiente_en_espera(lista_reservas, id_complejo, fecha, hora):
    """Devuelve el primero de la cola de espera de un turno.

    Parámetros:
        lista_reservas, id_complejo, fecha y hora del turno.
    Devuelve:
        El diccionario de la reserva más antigua en espera, o None si no hay ninguna.
    """
    # TODO [FED]: filtrar las que estén en_espera para ese turno y quedarse con la
    # de fecha_registro más vieja. Acá es donde la cola funciona como FIFO.
    return None


def confirmar_espera(lista_reservas, id_reserva):
    """Pasa una reserva de la lista de espera a confirmada.

    Parámetros:
        lista_reservas e id_reserva de la reserva en espera.
    Devuelve:
        Tupla (lista_reservas, True) si la confirmó, (lista_reservas, False) si no.
    """
    # TODO [FED]: verificar que el turno siga libre antes de confirmar.
    return lista_reservas, False
