# Contrato de módulos

**Zonda Bytes** — backend de CanchaYa

Propuesta de división del trabajo para el backend de CanchaYa. Define **qué función
expone cada módulo, qué recibe y qué devuelve**, para que los cuatro podamos programar en
paralelo sin pisarnos y sin esperar a que el otro termine.

Es una propuesta, no una imposición: si alguno necesita otra firma o un campo más, lo
hablamos y lo corregimos acá antes de escribir código. Lo importante es que **una vez
acordado, nadie cambie una firma sin avisar**, porque rompe el módulo del de al lado.

| Módulo | Responsable |
|---|---|
| `main.py` | Leandro Licata |
| `estructuras.py` | Federico Cabrera |
| `persistencia.py` | Gonzalo Tapia |
| `utils.py` | Gustavo Di Paola |
| `estadisticas.py` | Gustavo Di Paola |

## Reglas generales

1. **Solo `main.py` imprime en pantalla.** Los demás módulos calculan y devuelven valores;
   no usan `print()`. La única excepción son las funciones `pedir_*()` de `utils.py`, que
   por definición piden datos al usuario. Esto es lo que permite que el día de mañana la
   misma lógica se pueda usar desde la API con Flask sin tocar nada.
2. **`main.py` no tiene lógica de cálculo ni define estructuras de datos.** Solo menú,
   flujo y llamadas. Es un requisito explícito de la consigna.
3. **Importación:** `import persistencia` y después `persistencia.cargar_json(...)`.
   Nada de `from ... import *`, que oculta de dónde sale cada función.
4. **Nomenclatura `snake_case`** en variables, funciones y claves de diccionarios.
5. **Toda función lleva docstring** con qué hace, qué recibe y qué devuelve. Ninguna
   supera las 40 líneas.
6. **Las funciones no explotan:** si algo sale mal devuelven `None`, `False` o una lista
   vacía, y `main.py` decide qué mensaje mostrar.

## Estructuras de datos compartidas

Estos dos diccionarios son el idioma común. Los campos están tomados del formulario y del
listado del sitio, así que si mañana conectamos el frontend, coincide.

```python
complejo = {
    "id": 1,
    "nombre": "Estadio 5",
    "zona": "Godoy Cruz",
    "canchas": 3,
    "tipo": "sintetica",          # sintetica | techada | aire_libre
    "precio_hora": 18000
}

reserva = {
    "id": 1,
    "nombre_cliente": "Lionel Perez",
    "email": "lionel@ejemplo.com",
    "telefono": "261 123 4567",
    "id_complejo": 1,
    "fecha": "2026-09-25",              # siempre AAAA-MM-DD
    "hora": "20:00",
    "jugadores": 10,
    "comentarios": "",
    "estado": "confirmada",             # confirmada | cancelada | en_espera
    "fecha_registro": "2026-09-22 19:05:00",
    "motivo_cancelacion": ""
}
```

Las colecciones son **listas de diccionarios**: `lista_complejos` y `lista_reservas`.
Los horarios posibles son fijos, los mismos que ofrece el formulario:

```python
HORARIOS = ("18:00", "19:00", "20:00", "21:00", "22:00")
```

## `persistencia.py` — Gonzalo

Constantes que expone: `CARPETA_DATOS`, `RUTA_COMPLEJOS`, `RUTA_RESERVAS`, `RUTA_LOG`,
`RUTA_GRAFICO` (ocupación por horario, `graficos/ocupacion.png`) y
`RUTA_GRAFICO_INGRESOS` (ingresos por complejo, `graficos/ingresos.png`). *(La segunda se
agrega para el Hito 2; las dos se arman sobre `CARPETA_GRAFICOS`, como la primera.)*

| Función | Devuelve |
|---|---|
| `cargar_json(ruta, por_defecto=None)` | El contenido del archivo. Si no existe lo crea con `por_defecto` y devuelve eso. Captura `FileNotFoundError`, `IOError` y JSON corrupto. |
| `guardar_json(ruta, datos)` | `True` si pudo guardar, `False` si falló. |
| `exportar_csv(ruta, encabezados, filas)` | Cantidad de filas escritas, o `0` si falló. `filas` es una lista de listas. |
| `registrar_log(accion, detalle="")` | `None`. Agrega al `.txt` una línea `AAAA-MM-DD HH:MM:SS \| accion \| detalle`. |
| `ruta_reporte(fecha)` | La ruta del CSV de ese día: `datos/reporte_AAAA-MM-DD.csv`. |
| `importar_json()` | `True` si pudo cargar en la base los JSON de complejos y reservas. Lo llama `inicializar_bd()` cuando la base no existía, para que un clon nuevo arranque con datos. Usa `leer_json(ruta)`, que lee el archivo sin pasar por la base. *(Agregadas por Leandro para la API.)* |

Todo con bloque `with`. El programa tiene que arrancar aunque no exista ningún archivo.

## `estructuras.py` — Federico

| Función | Devuelve |
|---|---|
| `crear_reserva(lista_reservas, datos)` | El diccionario de la reserva armado, con `id` autoincremental, `fecha_registro` y `estado` inicial. `datos` es un diccionario con los campos que cargó el usuario. |
| `esta_ocupado(lista_reservas, id_complejo, fecha, hora)` | `True` / `False`. Solo cuentan las reservas `confirmada`. |
| `agregar_reserva(lista_reservas, reserva)` | Tupla `(lista_reservas, estado)`, donde `estado` es `"confirmada"` o `"en_espera"` según si el horario estaba libre. |
| `horarios_disponibles(lista_reservas, id_complejo, fecha)` | Lista de horas libres de `HORARIOS` para ese complejo y fecha. |
| `cancelar_reserva(lista_reservas, id_reserva, motivo)` | Tupla `(lista_reservas, True/False)`. Pasa el estado a `cancelada` y guarda el motivo. |
| `siguiente_en_espera(lista_reservas, id_complejo, fecha, hora)` | La primera reserva `en_espera` de ese turno (FIFO, por `fecha_registro`), o `None`. |
| `modificar_reserva(lista_reservas, id_reserva, campo, valor)` | Tupla `(lista_reservas, True/False)`. Solo se modifican `jugadores` y `comentarios`; para cambiar de horario se cancela y se reserva de nuevo. |
| `confirmar_espera(lista_reservas, id_reserva)` | Tupla `(lista_reservas, True/False)`. Pasa una reserva de `en_espera` a `confirmada` cuando el turno quedó libre. |
| `promover_espera(lista_reservas, reserva)` | Tupla `(lista_reservas, promovida)`. Confirma al primero de la cola del turno que liberó `reserva`; `promovida` es esa reserva, o `None` si no había nadie o el turno sigue ocupado. *(Agregada por Leandro para la API.)* |

Define además las constantes `HORARIOS`, `MIN_JUGADORES` y `MAX_JUGADORES`. Es el módulo donde vive la **cola FIFO**: al cancelarse una reserva, `main.py` y la API llaman a
`promover_espera()`, que le pasa el lugar al primero de la cola.

## `utils.py` — Gustavo

| Función | Devuelve |
|---|---|
| `pedir_texto(mensaje, largo_minimo=3)` | El texto validado. Reintenta hasta que sea válido. |
| `pedir_entero(mensaje, minimo, maximo)` | El número validado. Captura `ValueError`. |
| `pedir_opcion(mensaje, opciones)` | El elemento elegido de la lista `opciones`, que puede contener textos o números (ids). |
| `validar_email(texto)` | `True` / `False`. |
| `validar_fecha(texto)` | `True` / `False`. Valida que el formato `AAAA-MM-DD` sea correcto y que la fecha exista. Se usa en las búsquedas, donde sí valen fechas pasadas. |
| `validar_fecha_reserva(texto)` | `True` / `False`. Lo anterior y además que no sea una fecha pasada. Se usa al registrar. |
| `buscar_reservas(lista_reservas, campo, valor)` | Lista de las reservas cuyo `campo` coincide (parcial y sin distinguir mayúsculas para textos). |
| `ordenar_por(lista, campo, descendente=False)` | Lista ordenada. **Algoritmo propio de inserción**, no `sorted()`: suma puntos en la rúbrica. |
| `formatear_reserva(reserva, lista_complejos)` | Cadena de una línea, lista para imprimir, con el nombre del complejo en vez del id. |
| `fila_csv(reserva, lista_complejos)` | Lista de valores de la reserva para el CSV, en el orden de los encabezados. |
| `buscar_complejo(lista_complejos, id_complejo)` | El diccionario del complejo, o `None` si no existe. *(Agregada por Leandro para la API.)* |
| `validar_reserva(datos, lista_complejos)` | `None` si todos los campos son válidos, o un texto con el primer error. La usa la API, que recibe la reserva entera en un JSON y no puede pedir los datos de a uno. Se apoya en `es_texto_valido(valor, largo_minimo)` y `es_entero_en_rango(valor, minimo, maximo)`. *(Agregadas por Leandro para la API.)* |
| `validar_modificacion(campo, valor)` | `None` si el campo es editable y el valor es válido (jugadores entre `MIN_JUGADORES` y `MAX_JUGADORES`, comentarios de texto), o un texto con el error. `validar_reserva()` también la usa. *(Agregada por Leandro para la API.)* |

## `estadisticas.py` — Gustavo

| Función | Devuelve |
|---|---|
| `ocupacion_por_horario(lista_reservas)` | Diccionario `{"18:00": 4, "19:00": 7, ...}`. |
| `ingresos_por_complejo(lista_reservas, lista_complejos)` | Diccionario `{"Estadio 5": 54000, ...}`, con las confirmadas por el precio por hora. Busca cada complejo con `utils.buscar_complejo()`. |
| `ranking_complejos(lista_reservas, lista_complejos, tope=3)` | Lista de tuplas `(nombre, cantidad)` ordenada de mayor a menor. |
| `porcentaje_cancelaciones(lista_reservas)` | Número con un decimal. `0.0` si no hay reservas (ojo con la división por cero). |
| `graficar_barras(datos, titulo, etiqueta_x, etiqueta_y, ruta)` | `True` si generó el PNG, `False` si matplotlib no está instalado o no pudo escribir el archivo. `datos` es un diccionario `{etiqueta: valor}`; cada clave es una barra. Es la parte común de los dos gráficos, para no repetir el código de matplotlib. |
| `graficar_ocupacion(ocupacion, ruta)` | `True` si generó el PNG. Recibe lo que devuelve `ocupacion_por_horario()` y llama a `graficar_barras()`. |
| `graficar_ingresos(ingresos, ruta)` | `True` si generó el PNG. Recibe lo que devuelve `ingresos_por_complejo()` y llama a `graficar_barras()`. |

Los dos gráficos son el eje de investigación (Opción D — matplotlib), que pide **al menos
2 gráficos exportados como PNG**. matplotlib se importa solo dentro de `graficar_barras()`,
para que el resto del programa funcione aunque no esté instalado.

*Hito 2:* `buscar_complejo_por_id()` se elimina porque repetía `utils.buscar_complejo()`.
La consigna no permite código duplicado.

## `main.py` — Leandro

Solo menú y flujo. Una función por opción, que pide los datos con `utils`, llama a
`estructuras`, guarda con `persistencia` y muestra el resultado.

| Función | Qué hace |
|---|---|
| `mostrar_menu()` | Imprime las opciones. |
| `mostrar_submenu_consultas()` | Imprime el submenú de búsquedas. |
| `flujo_registrar_reserva(...)`, `flujo_consultar_disponibilidad(...)`, `flujo_consultas(...)`, `flujo_modificar_cancelar(...)`, `flujo_lista_espera(...)`, `flujo_estadisticas(...)`, `flujo_exportar_csv(...)` | Una por cada opción del menú. `flujo_estadisticas()` genera los dos gráficos, con `RUTA_GRAFICO` y `RUTA_GRAFICO_INGRESOS`. |
| `main()` | Carga los datos, corre el bucle `while` y guarda al salir. |

## Control de la consigna

| Requisito | Estado |
|---|---|
| Mínimo 4 módulos | 5 |
| Mínimo 10 funciones propias | 67 sin contar la API (79 con `api.py`) |
| Al menos 3 funciones por módulo (salvo `main.py`) | Cumple en los cuatro |
| Menú con 5+ funcionalidades y un submenú | 7 opciones + submenús de consultas y de modificar/cancelar |
| 1 búsqueda con filtro | `buscar_reservas()` |
| Ordenamiento propio | `ordenar_por()`, por inserción |
| Mínimo 2 estadísticas | 4 |
| Persistencia JSON + CSV + TXT | `persistencia.py` completo (más SQLite) |
| Eje D: al menos 2 gráficos PNG | `graficar_ocupacion()` y `graficar_ingresos()` *(la segunda, pendiente)* |
| Mínimo 5 pruebas unitarias | 37 con pytest; falta `test_estadisticas.py` |
