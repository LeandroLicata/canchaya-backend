# persistencia.py — Lectura y escritura de los archivos del programa (JSON, CSV y TXT).
# [GON] Gonzalo Tapia.
#
# ESQUELETO: las firmas son las acordadas en CONTRATO_MODULOS.md y main.py ya las usa.
# Cada función devuelve un valor neutro hasta que Gonzalo la implemente.

import os
import json
import csv
from datetime import datetime

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
    try:
       with open(ruta, "r", encoding="utf-8") as archivo:
           return json.load(archivo)
    except FileNotFoundError:
       guardar_json(ruta, por_defecto)
       return por_defecto
    except (json.JSONDecodeError, IOError, OSError):
        return por_defecto


def guardar_json(ruta, datos):
    """Guarda datos en un archivo JSON.

    Parámetros:
        ruta: ruta del archivo a escribir.
        datos: lista o diccionario a serializar.
    Devuelve:
        True si pudo guardar, False si falló.
    """
    try:
        carpeta = os.path.dirname(ruta)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
        return True
    except (IOError, OSError):
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
    try:
        carpeta = os.path.dirname(ruta)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)
        with open(ruta, "w",newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(encabezados)
            escritor.writerows(filas)
        return len(filas)
    except (IOError, OSError):
        return 0
    


def registrar_log(accion, detalle=""):
    """Agrega una línea al log de operaciones con la fecha y la hora.

    Parámetros:
        accion: nombre corto de la operación (por ejemplo "registrar_reserva").
        detalle: texto opcional con información extra.
    Devuelve:
        Nada.
    """
    try:
        carpeta = os.path.dirname(RUTA_LOG)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)
        momento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(RUTA_LOG, "a", encoding="utf-8") as archivo:
            archivo.write("{0} | {1} | {2}\n".format(momento, accion, detalle))
    except (IOError, OSError):
        pass
    return None
