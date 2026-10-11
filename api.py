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
    if not persistencia.guardar_json(persistencia.RUTA_RESERVAS, lista_reservas):
        return respuesta_error("No se pudo guardar la reserva. Probá de nuevo.", 500)
    persistencia.registrar_log("registrar_reserva", "#{0} {1} (web)".format(
        reserva["id"], estado))
    return jsonify(reserva), 201


if __name__ == "__main__":
    # threaded=False atiende un pedido por vez: guardar_tabla() reescribe la tabla
    # entera, y dos escrituras simultáneas podrían pisarse.
    app.run(port=5000, debug=True, threaded=False)
