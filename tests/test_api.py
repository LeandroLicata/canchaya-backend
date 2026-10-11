# tests/test_api.py — Pruebas de los endpoints de api.py con el cliente de Flask.
# [LEA] Leandro Licata.

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import api
import persistencia

COMPLEJOS = [
    {"id": 1, "nombre": "Estadio 5", "zona": "Godoy Cruz", "canchas": 3,
     "tipo": "sintetica", "precio_hora": 18000},
    {"id": 2, "nombre": "La Redonda", "zona": "Las Heras", "canchas": 2,
     "tipo": "techada", "precio_hora": 20000},
]


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    """Cliente de prueba de Flask sobre una base y un log temporales.

    Así las pruebas nunca tocan los datos reales de datos/.
    Devuelve: el cliente, que permite hacer pedidos sin levantar el servidor.
    """
    monkeypatch.setattr(persistencia, "RUTA_BD", str(tmp_path / "prueba.db"))
    monkeypatch.setattr(persistencia, "RUTA_LOG", str(tmp_path / "log.txt"))
    persistencia.guardar_tabla("complejos", COMPLEJOS)
    return api.app.test_client()


def test_listar_complejos(cliente):
    """Devuelve los complejos de la base en JSON."""
    respuesta = cliente.get("/api/complejos")
    assert respuesta.status_code == 200
    assert respuesta.get_json() == COMPLEJOS


def test_ruta_inexistente_responde_json(cliente):
    """Una ruta desconocida devuelve 404 con el formato de error de la API."""
    respuesta = cliente.get("/api/no-existe")
    assert respuesta.status_code == 404
    assert "error" in respuesta.get_json()


def test_cors_habilitado(cliente):
    """Las respuestas permiten que el frontend las lea desde otro origen."""
    origen = "http://127.0.0.1:5500"
    respuesta = cliente.get("/api/complejos", headers={"Origin": origen})
    assert respuesta.headers.get("Access-Control-Allow-Origin") in ("*", origen)
