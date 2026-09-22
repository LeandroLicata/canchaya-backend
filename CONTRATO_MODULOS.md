# Contrato de módulos

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

Constantes que expone: `CARPETA_DATOS`, `RUTA_COMPLEJOS`, `RUTA_RESERVAS`, `RUTA_LOG`.

| Función | Devuelve |
|---|---|
| `cargar_json(ruta, por_defecto=None)` | El contenido del archivo. Si no existe lo crea con `por_defecto` y devuelve eso. Captura `FileNotFoundError`, `IOError` y JSON corrupto. |
| `guardar_json(ruta, datos)` | `True` si pudo guardar, `False` si falló. |
| `exportar_csv(ruta, encabezados, filas)` | Cantidad de filas escritas, o `0` si falló. `filas` es una lista de listas. |
| `registrar_log(accion, detalle="")` | `None`. Agrega al `.txt` una línea `AAAA-MM-DD HH:MM:SS \| accion \| detalle`. |

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

Es el módulo donde vive la **cola FIFO**: al cancelarse una reserva, `main.py` pregunta
por `siguiente_en_espera()` y le ofrece el lugar.

## `utils.py` — Gustavo

| Función | Devuelve |
|---|---|
| `pedir_texto(mensaje, largo_minimo=3)` | El texto validado. Reintenta hasta que sea válido. |
| `pedir_entero(mensaje, minimo, maximo)` | El número validado. Captura `ValueError`. |
| `pedir_opcion(mensaje, opciones)` | El elemento elegido de la lista `opciones`. |
| `validar_email(texto)` | `True` / `False`. |
| `validar_fecha(texto)` | `True` / `False`. Formato `AAAA-MM-DD` y que no sea una fecha pasada. |
| `buscar_reservas(lista_reservas, campo, valor)` | Lista de las reservas cuyo `campo` coincide (parcial y sin distinguir mayúsculas para textos). |
| `ordenar_por(lista, campo, descendente=False)` | Lista ordenada. **Algoritmo propio de inserción**, no `sorted()`: suma puntos en la rúbrica. |
| `formatear_reserva(reserva, lista_complejos)` | Cadena de una línea, lista para imprimir, con el nombre del complejo en vez del id. |

## `estadisticas.py` — Gustavo

| Función | Devuelve |
|---|---|
| `ocupacion_por_horario(lista_reservas)` | Diccionario `{"18:00": 4, "19:00": 7, ...}`. |
| `ingresos_por_complejo(lista_reservas, lista_complejos)` | Diccionario `{"Estadio 5": 54000, ...}`, con las confirmadas por el precio por hora. |
| `ranking_complejos(lista_reservas, lista_complejos, tope=3)` | Lista de tuplas `(nombre, cantidad)` ordenada de mayor a menor. |
| `porcentaje_cancelaciones(lista_reservas)` | Número con un decimal. `0.0` si no hay reservas (ojo con la división por cero). |
| `graficar_ocupacion(ocupacion, ruta)` | `True` si generó el PNG. Es el eje de investigación (matplotlib). |

## `main.py` — Leandro

Solo menú y flujo. Una función por opción, que pide los datos con `utils`, llama a
`estructuras`, guarda con `persistencia` y muestra el resultado.

| Función | Qué hace |
|---|---|
| `mostrar_menu()` | Imprime las opciones. |
| `mostrar_submenu_consultas()` | Imprime el submenú de búsquedas. |
| `flujo_registrar_reserva(...)`, `flujo_consultar_disponibilidad(...)`, `flujo_consultas(...)`, `flujo_modificar_cancelar(...)`, `flujo_lista_espera(...)`, `flujo_estadisticas(...)`, `flujo_exportar_csv(...)` | Una por cada opción del menú. |
| `main()` | Carga los datos, corre el bucle `while` y guarda al salir. |

## Control de la consigna

| Requisito | Estado |
|---|---|
| Mínimo 4 módulos | 5 |
| Mínimo 10 funciones propias | 26 previstas |
| Al menos 3 funciones por módulo (salvo `main.py`) | Cumple en los cuatro |
| Menú con 5+ funcionalidades y un submenú | 7 opciones + submenú de consultas |
| 1 búsqueda con filtro | `buscar_reservas()` |
| Ordenamiento propio | `ordenar_por()`, por inserción |
| Mínimo 2 estadísticas | 4 |
| Persistencia JSON + CSV + TXT | `persistencia.py` completo |
