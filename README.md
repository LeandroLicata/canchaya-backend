# Sistema de Gestión de Turnos

Proyecto Integrador — Programación I
Tecnicatura Superior en Desarrollo de Software
IES 9-008 "Manuel Belgrano" — Ciclo lectivo 2026
Comisión: 1° Segunda (Martes)

## Integrantes

- Leandro Licata
- Federico Cabrera
- Gonzalo Tapia
- Gustavo Di Paola

## Descripción

Aplicación de consola en Python (programación estructurada, sin POO) para la gestión
de turnos de atención. Permite registrar pacientes/clientes, asignar turnos por orden
de llegada, buscar por DNI o nombre, consultar el historial de atenciones y generar
estadísticas de espera y atención por franja horaria.

Los datos se persisten en JSON, los reportes diarios se exportan en CSV y cada
operación del usuario queda registrada en un log de texto plano.

## Estado

Hito 0 — Pitch (martes 15 de septiembre de 2026). Repositorio creado.
El desarrollo comienza en la clase 2.

## Plan de trabajo

| Clase | Fecha | Actividad |
|-------|-------|-----------|
| 1 | 15/09 | **Hito 0 – Pitch.** Tema, integrantes y repositorio creado. |
| 2 | 22/09 | `main.py` con menú y `persistencia.py` con JSON. Al menos 1 funcionalidad operativa. |
| 3 | 29/09 | Completar funcionalidades, búsqueda/ordenamiento y estadísticas. |
| 4 | 06/10 | **Hito 1 – v1.0.** Menú + persistencia + 1 funcionalidad completa. |
| 5 | 13/10 | Exportación CSV, log TXT, pruebas unitarias y `PROMPTS.md`. |
| 6 | 20/10 | Refactorización, limpieza, video, README y documentación final. |
| 7 | 27/10 | **Hito 2 – Final.** Entrega completa y defensa oral. |

## Estructura prevista

```
main.py           # Menú principal y flujo de la aplicación
estructuras.py    # Estructuras de datos del dominio (cola de turnos, historial)
persistencia.py   # Lectura y escritura de archivos JSON, CSV y TXT
utils.py          # Validaciones, formateo, búsquedas y ordenamiento
estadisticas.py   # Cálculo de métricas sobre los turnos (a definir)
tests/            # Pruebas unitarias
```

## Eje de investigación

A definir con el equipo.

## Requisitos

- Python 3.10 o superior
- Bibliotecas estándar: `json`, `csv`, `datetime`, `os`

## Créditos de uso de IA

El uso de herramientas de IA durante el desarrollo se documenta en `PROMPTS.md`.
