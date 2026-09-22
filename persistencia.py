# persistencia.py — Lectura y escritura de los archivos del programa (JSON, CSV y TXT).
# [GON] Gonzalo Tapia.
#
# ESQUELETO: las firmas son las acordadas en CONTRATO_MODULOS.md y main.py ya las usa.
# Cada función devuelve un valor neutro hasta que Gonzalo la implemente.

import os

CARPETA_DATOS = "datos"
CARPETA_GRAFICOS = "graficos"
RUTA_COMPLEJOS = os.path.join(CARPETA_DATOS, "complejos.json")
RUTA_RESERVAS = os.path.join(CARPETA_DATOS, "reservas.json")
RUTA_LOG = os.path.join(CARPETA_DATOS, "log_operaciones.txt")
RUTA_GRAFICO = os.path.join(CARPETA_GRAFICOS, "ocupacion.png")


def ruta_reporte(fecha):
    """Arma la ruta del reporte CSV de un día.

    Parámetros:
        fecha: cadena con formato AAAA-MM-DD.
    Devuelve:
        La ruta del archivo, por ejemplo datos/reporte_2026-09-25.csv.
    """
    return os.path.join(CARPETA_DATOS, "reporte_{0}.csv".format(fecha))


def cargar_json(ruta, por_defecto=None):
    """Carga el contenido de un archivo JSON.

    Parámetros:
        ruta: ruta del archivo a leer.
        por_defecto: valor a devolver y a grabar si el archivo no existe.
    Devuelve:
        El contenido del archivo, o por_defecto si no existe o está dañado.
    """
    # TODO [GON]: abrir con `with`, leer con json.load() y capturar
    # FileNotFoundError, IOError y JSONDecodeError. Si el archivo no existe,
    # crearlo con `por_defecto` (la consigna exige que el programa arranque igual).
    return por_defecto


def guardar_json(ruta, datos):
    """Guarda datos en un archivo JSON.

    Parámetros:
        ruta: ruta del archivo a escribir.
        datos: lista o diccionario a serializar.
    Devuelve:
        True si pudo guardar, False si falló.
    """
    # TODO [GON]: json.dump() dentro de un `with`, con ensure_ascii=False e indent=2,
    # capturando IOError. Crear la carpeta si no existe (os.makedirs).
    return False


def exportar_csv(ruta, encabezados, filas):
    """Escribe un archivo CSV con los encabezados y las filas recibidas.

    Parámetros:
        ruta: ruta del archivo a generar.
        encabezados: lista con los nombres de las columnas.
        filas: lista de listas, una por cada fila de datos.
    Devuelve:
        La cantidad de filas escritas, o 0 si falló.
    """
    # TODO [GON]: csv.writer() dentro de un `with`, con newline="" y encoding utf-8,
    # capturando IOError.
    return 0


def registrar_log(accion, detalle=""):
    """Agrega una línea al log de operaciones con la fecha y la hora.

    Parámetros:
        accion: nombre corto de la operación (por ejemplo "registrar_reserva").
        detalle: texto opcional con información extra.
    Devuelve:
        Nada.
    """
    # TODO [GON]: abrir el TXT en modo "a" dentro de un `with` y escribir
    # "AAAA-MM-DD HH:MM:SS | accion | detalle" usando datetime.now().
    return None
