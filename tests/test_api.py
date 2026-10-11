# tests/test_api.py — Pruebas de los endpoints de api.py con el cliente de Flask.
# [LEA] Leandro Licata.

import os
import sys
from datetime import date, timedelta

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

MANANA = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")


def reserva_valida(**cambios):
    """Arma el JSON de una reserva válida para mañana, con los cambios que se pidan.

    Parámetros: los campos a reemplazar, como argumentos con nombre.
    Devuelve: el diccionario listo para mandar en el cuerpo del POST.
    """
    datos = {
        "nombre_cliente": "Lionel Perez",
        "email": "lionel@ejemplo.com",
        "telefono": "261 123 4567",
        "id_complejo": 1,
        "fecha": MANANA,
        "hora": "20:00",
        "jugadores": 10,
        "comentarios": "",
    }
    datos.update(cambios)
    return datos


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    """Cliente de prueba de Flask sobre una base y un log temporales.

    Así las pruebas nunca tocan los datos reales de datos/.
    Devuelve: el cliente, que permite hacer pedidos sin levantar el servidor.
    """
    monkeypatch.setattr(persistencia, "RUTA_BD", str(tmp_path / "prueba.db"))
    monkeypatch.setattr(persistencia, "RUTA_LOG", str(tmp_path / "log.txt"))
    # La base temporal es nueva y se llenaría con los JSON reales: se pisan las dos tablas.
    persistencia.guardar_tabla("complejos", COMPLEJOS)
    persistencia.guardar_tabla("reservas", [])
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


def test_disponibilidad_marca_los_ocupados(cliente):
    """Después de reservar las 20:00, ese horario deja de figurar como libre."""
    url = "/api/complejos/1/disponibilidad?fecha=" + MANANA
    assert cliente.get(url).get_json()["libres"] == ["18:00", "19:00", "20:00",
                                                     "21:00", "22:00"]
    cliente.post("/api/reservas", json=reserva_valida())
    respuesta = cliente.get(url)
    assert respuesta.status_code == 200
    assert "20:00" not in respuesta.get_json()["libres"]
    assert len(respuesta.get_json()["horarios"]) == 5


def test_disponibilidad_con_errores(cliente):
    """Complejo inexistente da 404; fecha faltante o inválida da 400."""
    assert cliente.get("/api/complejos/99/disponibilidad?fecha=" + MANANA).status_code == 404
    assert cliente.get("/api/complejos/1/disponibilidad").status_code == 400
    assert cliente.get("/api/complejos/1/disponibilidad?fecha=2026-02-30").status_code == 400


def test_registrar_reserva(cliente):
    """Una reserva válida se crea confirmada, se guarda en la base y se registra."""
    respuesta = cliente.post("/api/reservas", json=reserva_valida())
    assert respuesta.status_code == 201
    reserva = respuesta.get_json()
    assert reserva["id"] == 1
    assert reserva["estado"] == "confirmada"
    assert persistencia.cargar_tabla("reservas")[0]["nombre_cliente"] == "Lionel Perez"
    with open(persistencia.RUTA_LOG, encoding="utf-8") as archivo:
        assert "registrar_reserva" in archivo.read()


def test_reserva_invalida_o_sin_json(cliente):
    """Datos inválidos o un cuerpo que no es JSON dan 400 con el motivo del error."""
    respuesta = cliente.post("/api/reservas", json=reserva_valida(jugadores="10"))
    assert respuesta.status_code == 400
    assert "jugadores" in respuesta.get_json()["error"]
    assert cliente.post("/api/reservas", data="hola").status_code == 400
    assert persistencia.cargar_tabla("reservas") == []


def test_horario_ocupado_pide_aceptar_la_espera(cliente):
    """Con el turno tomado da 409, salvo que se acepte la lista de espera."""
    cliente.post("/api/reservas", json=reserva_valida())
    respuesta = cliente.post("/api/reservas", json=reserva_valida())
    assert respuesta.status_code == 409
    respuesta = cliente.post("/api/reservas", json=reserva_valida(aceptar_espera=True))
    assert respuesta.status_code == 201
    assert respuesta.get_json()["estado"] == "en_espera"
    assert len(persistencia.cargar_tabla("reservas")) == 2



def test_listar_buscar_y_ordenar(cliente):
    """Lista todas, filtra por cliente o complejo, y ordena por el campo pedido."""
    cliente.post("/api/reservas", json=reserva_valida(hora="21:00"))
    cliente.post("/api/reservas", json=reserva_valida(hora="18:00", id_complejo=2,
                                                     nombre_cliente="Ana Gomez"))
    assert len(cliente.get("/api/reservas").get_json()) == 2
    por_nombre = cliente.get("/api/reservas?campo=nombre_cliente&valor=ana").get_json()
    assert [r["nombre_cliente"] for r in por_nombre] == ["Ana Gomez"]
    por_complejo = cliente.get("/api/reservas?campo=id_complejo&valor=1").get_json()
    assert [r["id_complejo"] for r in por_complejo] == [1]
    ordenadas = cliente.get("/api/reservas?orden=hora&desc=1").get_json()
    assert [r["hora"] for r in ordenadas] == ["21:00", "18:00"]


def test_listar_con_parametros_invalidos(cliente):
    """Campo de búsqueda u orden desconocido, o id no numérico, dan 400."""
    assert cliente.get("/api/reservas?campo=telefono&valor=261").status_code == 400
    assert cliente.get("/api/reservas?campo=id_complejo&valor=uno").status_code == 400
    assert cliente.get("/api/reservas?orden=email").status_code == 400


def test_consultar_reserva(cliente):
    """Devuelve la reserva pedida, o 404 si el id no existe."""
    cliente.post("/api/reservas", json=reserva_valida())
    assert cliente.get("/api/reservas/1").get_json()["nombre_cliente"] == "Lionel Perez"
    assert cliente.get("/api/reservas/99").status_code == 404


def test_modificar_reserva(cliente):
    """Cambia jugadores o comentarios y lo guarda; otros campos o valores dan 400."""
    cliente.post("/api/reservas", json=reserva_valida())
    respuesta = cliente.patch("/api/reservas/1", json={"campo": "jugadores", "valor": 12})
    assert respuesta.status_code == 200
    assert respuesta.get_json()["jugadores"] == 12
    assert persistencia.cargar_tabla("reservas")[0]["jugadores"] == 12
    for cuerpo in ({"campo": "hora", "valor": "18:00"},
                   {"campo": "jugadores", "valor": 20},
                   {"campo": "comentarios", "valor": 5}):
        assert cliente.patch("/api/reservas/1", json=cuerpo).status_code == 400
    assert cliente.patch("/api/reservas/99",
                         json={"campo": "jugadores", "valor": 8}).status_code == 404


def test_cancelar_promueve_al_primero_en_espera(cliente):
    """Al cancelar, el primero de la cola pasa a confirmado y se informa cuál fue."""
    cliente.post("/api/reservas", json=reserva_valida())
    cliente.post("/api/reservas", json=reserva_valida(aceptar_espera=True))
    respuesta = cliente.post("/api/reservas/1/cancelar", json={"motivo": "Llueve"})
    assert respuesta.status_code == 200
    cuerpo = respuesta.get_json()
    assert cuerpo["reserva"]["estado"] == "cancelada"
    assert cuerpo["promovida"]["id"] == 2
    estados = [r["estado"] for r in persistencia.cargar_tabla("reservas")]
    assert estados == ["cancelada", "confirmada"]


def test_cancelar_con_errores(cliente):
    """Sin motivo da 400, id inexistente 404, y cancelar dos veces 409."""
    cliente.post("/api/reservas", json=reserva_valida())
    assert cliente.post("/api/reservas/1/cancelar", json={}).status_code == 400
    assert cliente.post("/api/reservas/99/cancelar",
                        json={"motivo": "Llueve"}).status_code == 404
    cliente.post("/api/reservas/1/cancelar", json={"motivo": "Llueve"})
    respuesta = cliente.post("/api/reservas/1/cancelar", json={"motivo": "Llueve"})
    assert respuesta.status_code == 409
    respuesta = cliente.patch("/api/reservas/1", json={"campo": "jugadores", "valor": 8})
    assert respuesta.status_code == 409
