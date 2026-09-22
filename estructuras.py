# estructuras.py — Estructuras de datos del dominio: reservas, disponibilidad
# y la cola FIFO de lista de espera.
# [FED] Federico Cabrera.
#
# ESQUELETO: las firmas son las acordadas en CONTRATO_MODULOS.md y main.py ya las usa.
# Cada función devuelve un valor neutro hasta que Federico la implemente.
# Sin clases: las reservas son diccionarios dentro de una lista.

HORARIOS = ("18:00", "19:00", "20:00", "21:00", "22:00")

ESTADO_CONFIRMADA = "confirmada"
ESTADO_CANCELADA = "cancelada"
ESTADO_EN_ESPERA = "en_espera"


def crear_reserva(lista_reservas, datos):
    """Arma el diccionario de una reserva nueva.

    Parámetros:
        lista_reservas: lista actual, para calcular el id autoincremental.
        datos: diccionario con los campos que cargó el usuario.
    Devuelve:
        El diccionario de la reserva, con id, fecha_registro y estado inicial.
    """
    # TODO [FED]: id = máximo id existente + 1 (1 si la lista está vacía),
    # fecha_registro con datetime.now(), estado inicial y motivo_cancelacion vacío.
    return {}


def esta_ocupado(lista_reservas, id_complejo, fecha, hora):
    """Indica si un turno ya está tomado.

    Parámetros:
        lista_reservas, id_complejo, fecha (AAAA-MM-DD) y hora (HH:MM).
    Devuelve:
        True si hay una reserva confirmada para ese turno, False si no.
    """
    # TODO [FED]: recorrer la lista y comparar los tres campos.
    # Solo cuentan las reservas con estado confirmada.
    return False


def horarios_disponibles(lista_reservas, id_complejo, fecha):
    """Calcula qué horarios quedan libres en un complejo para una fecha.

    Parámetros:
        lista_reservas, id_complejo y fecha (AAAA-MM-DD).
    Devuelve:
        Lista con las horas de HORARIOS que todavía no están ocupadas.
    """
    # TODO [FED]: recorrer HORARIOS y quedarse con las que no estén ocupadas.
    return []


def agregar_reserva(lista_reservas, reserva):
    """Agrega una reserva, confirmada o en lista de espera según haya lugar.

    Parámetros:
        lista_reservas: lista actual.
        reserva: diccionario devuelto por crear_reserva().
    Devuelve:
        Tupla (lista_reservas, estado), con estado "confirmada" o "en_espera".
    """
    # TODO [FED]: consultar esta_ocupado(), fijar el estado de la reserva,
    # agregarla a la lista y devolver la lista junto con el estado aplicado.
    return lista_reservas, ESTADO_CONFIRMADA


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
