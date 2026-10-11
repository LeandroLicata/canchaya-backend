# api.py — API REST de CanchaYa: expone la lógica del backend al frontend con Flask.
# [LEA] Leandro Licata.
#
# Cumple el mismo rol que main.py pero para la web: no tiene lógica de cálculo, solo
# recibe el pedido, llama a los demás módulos y devuelve JSON. Ningún endpoint guarda
# datos en memoria: cada pedido lee de la base y, si cambia algo, la vuelve a guardar,
# así la consola y la API pueden usarse sobre los mismos datos.
#
# Se levanta con:  python api.py   (queda escuchando en http://localhost:5000)

from flask import Flask, jsonify
from flask_cors import CORS

import persistencia

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


if __name__ == "__main__":
    # threaded=False atiende un pedido por vez: guardar_tabla() reescribe la tabla
    # entera, y dos escrituras simultáneas podrían pisarse.
    app.run(port=5000, debug=True, threaded=False)
