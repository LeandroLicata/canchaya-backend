# tests/test_persistencia.py — Pruebas del módulo de persistencia.
# [GON] Gonzalo Tapia.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import persistencia


def test_escribir_y_leer_json(tmp_path):
    ruta = str(tmp_path / "prueba.json")
    datos = [{"id": 1, "nombre": "Estadio 5"}]

    assert persistencia.escribir_json(ruta, datos) is True
    assert persistencia.cargar_json(ruta) == datos
    
    
def test_guardar_y_cargar_tabla(tmp_path, monkeypatch):
    monkeypatch.setattr(persistencia, "RUTA_BD", str(tmp_path / "prueba.db"))
    
    complejos = [
        {"id": 1, "nombre": "Estadio 5", "zona": " Godoy Cruz", "canchas": 3, "tipo": "sintetica", "precio_hora": 18000}
    ]
    
    
    assert persistencia.guardar_tabla("complejos", complejos) is True
    assert persistencia.cargar_tabla("complejos") == complejos
    

def test_exportar_csv(tmp_path):
    ruta = str(tmp_path / "reporte.csv")
    encabezados = ["id", "ciente"]
    filas = [[1, "Gonzalo "], [2, "Pepe Hongo"]]
    
    assert persistencia.exportar_csv(ruta, encabezados, filas) == 2
    
    with open(ruta, "r", encoding="utf-8") as archivo:
        lineas = archivo.read().splitlines()
    assert len(lineas) == 3
    
    
def test_registrar_log_acumula(tmp_path, monkeypatch):
    ruta = str(tmp_path / "log.txt")
    monkeypatch.setattr(persistencia, "RUTA_LOG", ruta)
    
    persistencia.registrar_log("prueba", "primera")
    persistencia.registrar_log("prueba", "segunda")
    
    with open(ruta, "r", encoding="utf-8") as archivo:
        lineas = archivo.read().splitlines()
    assert len(lineas) == 2
    assert "primera" in lineas[0]
    assert "segunda" in lineas[1]
    
    
def test_cargar_json_inexistente(tmp_path):
    ruta = str(tmp_path / "nuevo.json")
    
    
    assert persistencia.cargar_json(ruta, []) == []
    assert os.path.exists(ruta) is True
    