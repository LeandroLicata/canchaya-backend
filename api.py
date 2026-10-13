# api.py — API REST de CanchaYa: expone la lógica del backend al frontend con Flask.
# [LEA] Leandro Licata.
#
# Cumple el mismo rol que main.py pero para la web: no tiene lógica de cálculo, solo
# recibe el pedido, llama a los demás módulos y devuelve JSON. Ningún endpoint guarda
# datos en memoria: cada pedido lee de la base y, si cambia algo, la vuelve a guardar,
# así la consola y la API pueden usarse sobre los mismos datos.
#
# Se levanta con:  python api.py   (queda escuchando en http://localhost:5000)

from flask import Flask, jsonify, request
from flask_cors import CORS

import estructuras
import persistencia
import utils

app = Flask(__name__)
# El frontend se abre desde otro origen (Live Server, otro puerto), y sin CORS el
# navegador bloquea las respuestas. Solo se habilita para las rutas de la API.
CORS(app, resources={r"/api/*": {"origins": "*"}})


def respuesta_error(mensaje, codigo):
    """Arma una respuesta de error con el mismo formato en toda la API.

    Parámetros:
        mensaje: texto que explica el error, pensado para mostrarlo al usuario.
        codigo: código de estado HTTP (400, 404, 409...).
    Devuelve:
        Tupla (respuesta JSON {"error": mensaje}, codigo), que Flask sabe enviar.
    """
    return jsonify({"error": mensaje}), codigo


def leer_cuerpo():
    """Lee el JSON que viene en el cuerpo del pedido.

    No recibe parámetros: lo toma del pedido en curso.
    Devuelve: el diccionario recibido, o None si no vino un objeto JSON válido.
    """
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return None
    return datos


def guardar_reservas(lista_reservas):
    """Guarda la lista de reservas en la base.

    Parámetros: la lista de reservas actualizada.
    Devuelve: None si pudo guardar, o la respuesta de error 500 lista para enviar.
    """
    if persistencia.guardar_json(persistencia.RUTA_RESERVAS, lista_reservas):
        return None
    return respuesta_error("No se pudieron guardar los cambios. Probá de nuevo.", 500)


@app.errorhandler(404)
def ruta_inexistente(error):
    """Responde en JSON cuando se pide una ruta que no existe.

    Parámetros: el error que genera Flask (no se usa, pero Flask lo pasa siempre).
    Devuelve: la respuesta de error con código 404.
    """
    return respuesta_error("La ruta pedida no existe.", 404)


@app.errorhandler(500)
def error_interno(error):
    """Responde en JSON si algo falla inesperadamente dentro de un endpoint.

    Parámetros: el error que genera Flask.
    Devuelve: la respuesta de error con código 500.
    """
    return respuesta_error("Ocurrió un error inesperado en el servidor.", 500)


@app.route("/api/complejos", methods=["GET"])
def listar_complejos():
    """Devuelve todos los complejos, para armar el listado y el formulario del sitio.

    No recibe parámetros.
    Devuelve: lista JSON de complejos con código 200.
    """
    lista_complejos = persistencia.cargar_json(persistencia.RUTA_COMPLEJOS, [])
    return jsonify(lista_complejos), 200


@app.route("/api/complejos/<int:id_complejo>/disponibilidad", methods=["GET"])
def consultar_disponibilidad(id_complejo):
    """Devuelve los horarios del día y cuáles siguen libres en un complejo.

    Parámetros:
        id_complejo: viene en la ruta. La fecha llega como ?fecha=AAAA-MM-DD.
    Devuelve:
        JSON con id_complejo, fecha, horarios (todos) y libres, con código 200;
        404 si el complejo no existe o 400 si la fecha es inválida.
    """
    lista_complejos = persistencia.cargar_json(persistencia.RUTA_COMPLEJOS, [])
    if utils.buscar_complejo(lista_complejos, id_complejo) is None:
        return respuesta_error("El complejo elegido no existe.", 404)
    fecha = request.args.get("fecha", "")
    if not utils.validar_fecha(fecha):
        return respuesta_error("La fecha no es válida (formato AAAA-MM-DD).", 400)
    lista_reservas = persistencia.cargar_json(persistencia.RUTA_RESERVAS, [])
    libres = estructuras.horarios_disponibles(lista_reservas, id_complejo, fecha)
    return jsonify({
        "id_complejo": id_complejo,
        "fecha": fecha,
        "horarios": list(estructuras.HORARIOS),
        "libres": libres,
    }), 200


@app.route("/api/reservas", methods=["POST"])
def registrar_reserva():
    """Registra una reserva nueva enviada por el formulario del sitio.

    Recibe en el cuerpo un JSON con los campos de la reserva. Si el horario está
    ocupado, solo se anota en la lista de espera cuando viene "aceptar_espera": true,
    igual que en la consola, donde se le pregunta al usuario.
    Devuelve:
        La reserva creada con código 201 (su "estado" dice si quedó confirmada o en
        espera); 400 si los datos son inválidos, 409 si el horario está ocupado y no
        se aceptó la espera, 500 si no se pudo guardar.
    """
    datos = request.get_json(silent=True)
    lista_complejos = persistencia.cargar_json(persistencia.RUTA_COMPLEJOS, [])
    error = utils.validar_reserva(datos, lista_complejos)
    if error is not None:
        return respuesta_error(error, 400)
    lista_reservas = persistencia.cargar_json(persistencia.RUTA_RESERVAS, [])
    ocupado = estructuras.esta_ocupado(lista_reservas, datos["id_complejo"],
                                       datos["fecha"], datos["hora"])
    if ocupado and datos.get("aceptar_espera") is not True:
        return respuesta_error("Ese horario está ocupado. Podés anotarte en la lista "
                               "de espera.", 409)
    reserva = estructuras.crear_reserva(lista_reservas, datos)
    lista_reservas, estado = estructuras.agregar_reserva(lista_reservas, reserva)
    error_guardado = guardar_reservas(lista_reservas)
    if error_guardado is not None:
        return error_guardado
    persistencia.registrar_log("registrar_reserva", "#{0} {1} (web)".format(
        reserva["id"], estado))
    return jsonify(reserva), 201


CAMPOS_BUSQUEDA = ("nombre_cliente", "email", "id_complejo", "fecha", "estado")
CAMPOS_ORDEN = ("id", "fecha", "hora", "nombre_cliente", "fecha_registro")


@app.route("/api/reservas", methods=["GET"])
def listar_reservas():
    """Lista las reservas, con búsqueda y orden opcionales.

    Recibe por la URL: ?campo=...&valor=... para filtrar (con utils.buscar_reservas)
    y ?orden=...&desc=1 para ordenar (con utils.ordenar_por; por defecto, por fecha).
    Devuelve:
        Lista JSON de reservas con código 200, o 400 si algún parámetro es inválido.
    """
    lista_reservas = persistencia.cargar_json(persistencia.RUTA_RESERVAS, [])
    campo = request.args.get("campo", "")
    valor = request.args.get("valor", "")
    if campo:
        if campo not in CAMPOS_BUSQUEDA:
            return respuesta_error("No se puede buscar por ese campo.", 400)
        if campo == "id_complejo":
            try:
                valor = int(valor)
            except ValueError:
                return respuesta_error("El id del complejo debe ser un número.", 400)
        lista_reservas = utils.buscar_reservas(lista_reservas, campo, valor)
    orden = request.args.get("orden", "fecha")
    if orden not in CAMPOS_ORDEN:
        return respuesta_error("No se puede ordenar por ese campo.", 400)
    descendente = request.args.get("desc", "") == "1"
    return jsonify(utils.ordenar_por(lista_reservas, orden, descendente)), 200


@app.route("/api/reservas/<int:id_reserva>", methods=["GET"])
def consultar_reserva(id_reserva):
    """Devuelve una reserva por su id.

    Parámetros: id_reserva, que viene en la ruta.
    Devuelve: la reserva con código 200, o 404 si no existe.
    """
    lista_reservas = persistencia.cargar_json(persistencia.RUTA_RESERVAS, [])
    reserva = estructuras.buscar_reserva_por_id(lista_reservas, id_reserva)
    if reserva is None:
        return respuesta_error("La reserva no existe.", 404)
    return jsonify(reserva), 200


@app.route("/api/reservas/<int:id_reserva>", methods=["PATCH"])
def modificar_reserva(id_reserva):
    """Modifica los jugadores o los comentarios de una reserva.

    Recibe en el cuerpo un JSON {"campo": ..., "valor": ...}. Para cambiar de horario
    se cancela y se reserva de nuevo, igual que en la consola.
    Devuelve:
        La reserva actualizada con código 200; 400 si los datos son inválidos, 404 si
        no existe, 409 si está cancelada, 500 si no se pudo guardar.
    """
    datos = leer_cuerpo()
    if datos is None:
        return respuesta_error("Los datos tienen un formato inválido.", 400)
    error = utils.validar_modificacion(datos.get("campo"), datos.get("valor"))
    if error is not None:
        return respuesta_error(error, 400)
    lista_reservas = persistencia.cargar_json(persistencia.RUTA_RESERVAS, [])
    reserva = estructuras.buscar_reserva_por_id(lista_reservas, id_reserva)
    if reserva is None:
        return respuesta_error("La reserva no existe.", 404)
    lista_reservas, modificada = estructuras.modificar_reserva(
        lista_reservas, id_reserva, datos["campo"], datos["valor"])
    if not modificada:
        return respuesta_error("No se puede modificar una reserva cancelada.", 409)
    error_guardado = guardar_reservas(lista_reservas)
    if error_guardado is not None:
        return error_guardado
    persistencia.registrar_log("modificar_reserva", "#{0} {1} (web)".format(
        id_reserva, datos["campo"]))
    return jsonify(reserva), 200


@app.route("/api/reservas/<int:id_reserva>/cancelar", methods=["POST"])
def cancelar_reserva(id_reserva):
    """Cancela una reserva y pasa el turno al primero de la lista de espera.

    Recibe en el cuerpo un JSON {"motivo": ...}.
    Devuelve:
        JSON {"reserva": la cancelada, "promovida": la que pasó a confirmada o null}
        con código 200; 400 si falta el motivo, 404 si no existe, 409 si ya estaba
        cancelada, 500 si no se pudo guardar.
    """
    datos = leer_cuerpo()
    if datos is None or not utils.es_texto_valido(datos.get("motivo"), 3):
        return respuesta_error("Indicá el motivo (al menos 3 caracteres).", 400)
    lista_reservas = persistencia.cargar_json(persistencia.RUTA_RESERVAS, [])
    reserva = estructuras.buscar_reserva_por_id(lista_reservas, id_reserva)
    if reserva is None:
        return respuesta_error("La reserva no existe.", 404)
    lista_reservas, cancelada = estructuras.cancelar_reserva(
        lista_reservas, id_reserva, datos["motivo"])
    if not cancelada:
        return respuesta_error("La reserva ya estaba cancelada.", 409)
    lista_reservas, promovida = estructuras.promover_espera(lista_reservas, reserva)
    error_guardado = guardar_reservas(lista_reservas)
    if error_guardado is not None:
        return error_guardado
    persistencia.registrar_log("cancelar_reserva", "#{0} (web)".format(id_reserva))
    if promovida is not None:
        persistencia.registrar_log("confirmar_espera", "#{0} (web)".format(promovida["id"]))
    return jsonify({"reserva": reserva, "promovida": promovida}), 200


if __name__ == "__main__":
    # threaded=False atiende un pedido por vez: guardar_tabla() reescribe la tabla
    # entera, y dos escrituras simultáneas podrían pisarse.
    app.run(port=5000, debug=True, threaded=False)
