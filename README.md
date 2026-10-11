<p align="center">
  <img src="assets/logo-zonda-bytes.png" alt="Zonda Bytes" width="420">
</p>

# CanchaYa — Backend

Proyecto de **Zonda Bytes**

Proyecto Integrador — Programación I<br>
Tecnicatura Superior en Desarrollo de Software<br>
IES 9-008 "Manuel Belgrano" — Ciclo lectivo 2026<br>
Comisión: 1° 2°

## Integrantes

| Integrante | Módulo a cargo |
|---|---|
| Leandro Licata | `main.py` — menú, flujo e integración |
| Federico Cabrera | `estructuras.py` — reservas, disponibilidad y lista de espera |
| Gonzalo Tapia | `persistencia.py` — JSON, CSV y TXT |
| Gustavo Di Paola | `utils.py` y `estadisticas.py` — validaciones, búsquedas y métricas |

Cada integrante versiona su propio trabajo con commits a su nombre. Los archivos `.py`
llevan en la cabecera la marca de responsable, igual que en el frontend (`[LEA]`, `[FED]`,
`[GON]`, `[GUS]`).

## Descripción

Backend en Python de **CanchaYa**, la plataforma de reserva de canchas de fútbol 5 en
Mendoza desarrollada por el mismo equipo en Práctica Profesional I
([sitio](https://github.com/gustavodipaola75-star/canchaya)).

Hoy el sitio es estático: el formulario de `reservar.html` valida los datos en el
navegador pero no los envía a ningún lado, y el listado de complejos está escrito a mano
en el HTML. Este proyecto resuelve esa mitad faltante: una aplicación de consola
(programación estructurada, **sin POO**) que administra los complejos, controla la
disponibilidad horaria, registra las reservas y produce estadísticas de ocupación.

Los datos se persisten en JSON, los reportes diarios se exportan en CSV y cada operación
queda registrada en un log de texto plano.

## Menú principal

1. **Registrar reserva** — valida los datos y verifica que el horario esté libre.
2. **Consultar disponibilidad** — horarios libres y ocupados de un complejo en una fecha.
3. **Consultas y búsquedas** *(submenú)* — por cliente, por complejo o por rango de fechas.
4. **Modificar o cancelar una reserva** — con motivo de cancelación.
5. **Lista de espera** — cola FIFO para los horarios ya ocupados; al liberarse uno, avanza
   el primero de la cola.
6. **Estadísticas del período** — ocupación, ingresos y rankings.
7. **Exportar reporte diario a CSV**.
0. Salir.

## Datos del dominio

Tomados del sitio, para que backend y frontend hablen de lo mismo:

- **Complejo:** nombre, zona, cantidad y tipo de canchas, precio por hora.
  Los seis de `complejos.html` (Estadio 5, La Redonda, Golazo Fútbol, El Potrero,
  Mundial F5, La Bombonerita).
- **Reserva:** cliente (nombre, email, teléfono), complejo, fecha, horario, cantidad de
  jugadores, comentarios y estado (confirmada, cancelada o en espera).
- **Horarios:** de 18:00 a 22:00, los mismos que ofrece el formulario.

## Estadísticas

- Ocupación por franja horaria (qué horarios se llenan y cuáles quedan vacíos).
- Ingresos estimados por complejo, según precio por hora y reservas confirmadas.
- Ranking de complejos más reservados.
- Porcentaje de reservas canceladas.

Las dos primeras se exportan además como gráficos PNG (ver eje de investigación).

## Estructura prevista

```
main.py           # Menú principal y flujo de la aplicación
estructuras.py    # Reservas, disponibilidad y lista de espera (cola FIFO)
persistencia.py   # Lectura y escritura de archivos JSON, CSV y TXT
utils.py          # Validaciones, formateo, búsquedas y ordenamiento
estadisticas.py   # Cálculo de métricas y gráficos de las reservas
api.py            # Endpoints Flask (eje complementario)
datos/            # complejos.json, reservas.json, reportes CSV y log TXT
graficos/         # Gráficos PNG generados con matplotlib
tests/            # Pruebas unitarias
```

## Eje de investigación

**Opción D — Visualización de datos con matplotlib** *(eje principal)*. Es el eje
investigado por el equipo y el declarado en el pitch. A partir de las estadísticas se
generan gráficos exportados como PNG: ocupación por franja horaria e ingresos por
complejo. Es el que se desarrolla en el informe.

**Opción C — API propia con Flask** *(complemento, si el tiempo lo permite)*. Exponer
como endpoints dos funcionalidades —consultar complejos y registrar una reserva— para que
el formulario de CanchaYa deje de ser una maqueta y envíe los datos a este backend. El
núcleo del proyecto sigue siendo la aplicación de consola; la API es una segunda puerta
de entrada a la misma lógica.

## Plan de trabajo

| Clase | Fecha | Actividad |
|-------|-------|-----------|
| 1 | 15/09 | **Hito 0 – Pitch.** Tema, integrantes y repositorio creado. |
| 2 | 22/09 | `main.py` con menú y `persistencia.py` con JSON. Al menos 1 funcionalidad operativa. |
| 3 | 29/09 | Disponibilidad, lista de espera, búsquedas, ordenamiento y estadísticas. |
| 4 | 06/10 | **Hito 1 – v1.0.** Menú + persistencia + 1 funcionalidad completa. |
| 5 | 13/10 | Exportación CSV, log TXT, pruebas unitarias y `PROMPTS.md`. |
| 6 | 20/10 | Gráficos con matplotlib, endpoints Flask, refactorización y documentación final. |
| 7 | 27/10 | **Hito 2 – Final.** Entrega completa y defensa oral. |

## Requisitos

- Python 3.10 o superior
- Bibliotecas estándar: `json`, `csv`, `datetime`, `os`
- `matplotlib` (eje principal), `flask` y `flask-cors` (API), `pytest` (pruebas),
  listadas en `requirements.txt`

Las dependencias se instalan en un entorno virtual dentro del proyecto, para que todo el
equipo use las mismas versiones sin tocar el Python de la máquina (la carpeta `.venv` está
en el `.gitignore`). En PowerShell, desde la carpeta del proyecto:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Se crea una sola vez; después alcanza con activarlo (`.venv\Scripts\Activate.ps1`) en cada
terminal nueva. En VS Code: `Ctrl+Shift+P` → *Python: Select Interpreter* → el de `.venv`,
y la terminal integrada lo activa sola. Si PowerShell no deja ejecutar `Activate.ps1`,
correr una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Cómo se ejecuta

- Aplicación de consola: `python main.py`
- API para el frontend: `python api.py` (queda escuchando en `http://localhost:5000`)
- Pruebas: `python -m pytest`

| Endpoint | Qué devuelve |
|---|---|
| `GET /api/complejos` | Lista de complejos |
| `GET /api/complejos/<id>/disponibilidad?fecha=AAAA-MM-DD` | `horarios` del día y cuáles están `libres` |
| `POST /api/reservas` | Crea la reserva (201). Si el horario está ocupado responde 409, salvo que venga `"aceptar_espera": true`, y entonces queda `en_espera` |
| `GET /api/reservas?campo=&valor=&orden=&desc=1` | Reservas, con búsqueda opcional (por `nombre_cliente`, `email`, `id_complejo`, `fecha` o `estado`) y orden (por defecto, por fecha) |
| `GET /api/reservas/<id>` | Una reserva |
| `PATCH /api/reservas/<id>` | Cambia `jugadores` o `comentarios`: `{"campo": ..., "valor": ...}` |
| `POST /api/reservas/<id>/cancelar` | Cancela con `{"motivo": ...}` y devuelve `{"reserva", "promovida"}`, el que pasó de la lista de espera a confirmado |

Los errores siempre vuelven en JSON con la forma `{"error": "mensaje"}`.

## Créditos de uso de IA

El uso de herramientas de IA durante el desarrollo se documenta en `PROMPTS.md`.
