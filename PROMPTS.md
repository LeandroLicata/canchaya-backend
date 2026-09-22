# Registro de uso de IA

**Zonda Bytes** — backend de CanchaYa

Bitácora de los usos significativos de inteligencia artificial en el desarrollo del
backend de CanchaYa, según el punto 5.2 de la consigna. Cada entrada anota la fecha, la
herramienta, el prompt, el resultado, las modificaciones que hizo el equipo y el estado
final de ese código.

Las consultas triviales no se registran. Sí se registra toda generación de código, diseño
de funciones o resolución de errores en la que haya participado una IA.

---

**Fecha:** 14/09/2026 | **Herramienta:** Claude (Claude Code) | **Integrante:** Leandro Licata

**Prompt:** "Tengo que crear un repo en GitHub para el proyecto integrador según lo que
dice `Proyecto_Integrador_1Segunda_Martes.docx`. De momento no hace falta que tenga nada,
ya que es para el Hito 0. Elegimos el tema Sistema de gestión de turnos."

**Resultado:** Leyó el archivo de la consigna y creó el repositorio público
`proyecto-integrador-turnos` con un `README.md` (tema, integrantes, descripción, plan de
trabajo clase por clase con las fechas del cronograma y estructura de módulos prevista) y
un `.gitignore`. Primer commit del proyecto.

**Modificaciones:** El equipo definió el nombre del repositorio, la visibilidad pública y
los nombres de los cuatro integrantes. Se contrastaron contra la consigna dos
observaciones que hizo la IA: que el equipo tiene 4 integrantes cuando se piden de 2 a 3,
y que faltaba definir el eje de investigación. El README se siguió corrigiendo en las
clases posteriores.

**Estado:** Se usó como base, modificado varias veces después.

---

**Fecha:** 22/09/2026 | **Herramienta:** Claude (Claude Code) | **Integrante:** Leandro Licata

**Prompt:** "Este repo ahora va a ser el backend de CanchaYa, proyecto en el que
trabajamos en Práctica Profesional I, que está en D:\Codigo\canchaya, pero vamos a
mantener la estructura y forma de trabajo."

**Resultado:** Leyó el frontend del sitio (`reservar.html` y `complejos.html`) y reescribió
el README con el dominio de reservas de canchas, tomando los campos del formulario y los
seis complejos del listado. Propuso además cambiar el eje de investigación de la Opción D
(matplotlib) a la Opción C (Flask), por tratarse de un backend.

**Modificaciones:** Se rechazó el cambio de eje. Se mantuvo matplotlib como eje principal
porque es el que el equipo ya investigó y el que figura en el documento del Hito 0 ya
entregado; Flask quedó como complemento opcional. Se verificó que el nombre correcto del
proyecto es "CanchaYa" y no "CanchasYa", como figura en el sitio.

**Estado:** Código modificado parcialmente. Se usó como base.

---

**Fecha:** 22/09/2026 | **Herramienta:** Claude (Claude Code) | **Integrante:** Leandro Licata

**Prompt:** "Comencemos con el contrato de módulos" — definir qué función expone cada
módulo, qué parámetros recibe y qué devuelve, para poder repartir el trabajo entre los
cuatro integrantes sin pisarnos.

**Resultado:** Generó `CONTRATO_MODULOS.md` con las firmas de las funciones de los cinco
módulos, los dos diccionarios compartidos (`complejo` y `reserva`), seis reglas de
convención y una tabla de control contra los requisitos de la consigna.

**Modificaciones:** _(completar: revisar si las firmas propuestas son las que el equipo
acepta, y anotar qué se cambió después de hablar con Federico, Gonzalo y Gustavo.)_

**Estado:** _(completar)_

---

**Fecha:** 22/09/2026 | **Herramienta:** Claude (Claude Code) | **Integrante:** Leandro Licata

**Prompt:** "Seguí con main.py" — escribir el módulo principal contra el contrato
acordado, respetando que no puede contener lógica de cálculo.

**Resultado:** Generó `main.py` con 17 funciones: menú de 7 opciones más salida, dos
submenús, una función `pedir_validado()` que centraliza el bucle de reintento, y
`try/except` sobre `KeyboardInterrupt`.

**Errores encontrados y corregidos durante la generación:** al escribir los flujos se
detectó que `validar_fecha()`, tal como estaba definida en el contrato, rechazaba las
fechas pasadas. Eso sirve al registrar una reserva, pero rompía la búsqueda por fecha en
el historial, que justamente consulta fechas ya pasadas. Se partió en dos funciones:
`validar_fecha()` (solo formato) y `validar_fecha_reserva()` (además, que no sea pasada).
También faltaban en el contrato `modificar_reserva()`, `confirmar_espera()`,
`ruta_reporte()`, la constante `RUTA_GRAFICO` y `fila_csv()`: sin ellas, las opciones 4, 5
y 7 del menú no se podían implementar. El contrato se actualizó.

**Verificación:** se revisó con un análisis del árbol sintáctico que las 17 funciones
tuvieran docstring, que ninguna superara las 40 líneas (la más larga tiene 25) y que las
32 llamadas a otros módulos estuvieran declaradas en el contrato.

**Modificaciones:** _(completar: anotar qué partes del flujo se cambiaron al leerlo y
probarlo, por ejemplo mensajes, orden de los datos que se piden o nombres de funciones.)_

**Estado:** _(completar)_

---

**Fecha:** 22/09/2026 | **Herramienta:** Claude (Claude Code) | **Integrante:** Leandro Licata

**Prompt:** Armar el esqueleto de los módulos restantes, con las firmas y los docstrings
vacíos, para poder ejecutar el programa sin escribir el código de los otros integrantes.

**Resultado:** Generó `estructuras.py`, `persistencia.py`, `utils.py` y `estadisticas.py`
con las firmas del contrato, un `TODO` con la sigla del responsable en cada función y el
valor de retorno neutro. Generó también `datos/complejos.json` con los seis complejos
tomados del sitio.

**Punto a tener en cuenta:** los stubs de `utils.py` no devuelven valores neutros a
propósito. Los validadores devuelven `True` y `pedir_opcion()` devuelve `"0"`, porque si
devolvieran `False` y `None` el bucle de reintento de `pedir_validado()` y el `while` del
menú quedarían girando para siempre. Está aclarado en la cabecera del archivo y hay que
reemplazarlos al implementar.

**Supuesto a confirmar:** en `datos/complejos.json` se cargó `tipo: "sintetica"` para
Golazo Fútbol, Mundial F5 y La Bombonerita. El sitio no especifica el tipo de cancha de
esos tres. Los otros tres están tomados textualmente del HTML.

**Modificaciones:** _(completar)_

**Estado:** _(completar)_

---

**Fecha:** 22/09/2026 | **Herramienta:** Claude | **Integrante:** Federico Cabrera

**Prompt:** "Necesito completar mi parte (soy Federico Cabrera)" — con el enlace al
repositorio. La IA leyó `CLAUDE.md`, `CONTRATO_MODULOS.md` y `main.py` para ubicar qué
módulo me toca y cómo lo usa el resto del programa.

**Resultado:** Implementó las ocho funciones de `estructuras.py` con las firmas del
contrato, sin cambiar ninguna: `crear_reserva()`, `esta_ocupado()`,
`horarios_disponibles()`, `agregar_reserva()`, `cancelar_reserva()`,
`modificar_reserva()`, `siguiente_en_espera()` y `confirmar_espera()`. Agregó tres
funciones internas para no repetir código: `buscar_reserva_por_id()` (la usan cancelar,
modificar y confirmar), `es_del_turno()` (la usan `esta_ocupado()` y
`siguiente_en_espera()`) y `valor_valido()` (controla el tipo del dato en
`modificar_reserva()`). Generó también `tests/test_estructuras.py` con 9 pruebas
unitarias con `unittest`.

**Decisiones de diseño que tomó y que hay que poder explicar en la defensa:**

- El id nuevo es el máximo existente + 1 y no `len(lista) + 1`, para no repetir un id si
  alguna vez se borra una reserva de la lista.
- La cola FIFO no es una lista aparte: son las reservas con estado `en_espera` de un mismo
  turno. `siguiente_en_espera()` recorre la lista y se queda con la de `fecha_registro`
  más vieja, sin usar `sorted()`. La fecha con formato `AAAA-MM-DD HH:MM:SS` se compara
  como texto; si dos reservas se registraron en el mismo segundo, desempata el id.
- `confirmar_espera()` vuelve a verificar que el turno esté libre aunque `main.py` ya lo
  controle, para que nunca haya dos reservas confirmadas en el mismo turno.
- `cancelar_reserva()` también acepta reservas en espera (el cliente sale de la cola) y
  devuelve `False` si la reserva ya estaba cancelada.
- `modificar_reserva()` rechaza tipos incorrectos (por ejemplo `"8"` como texto en
  `jugadores`) y descarta `True`/`False`, porque en Python `bool` es un tipo de `int`.

**Verificación:** las 9 pruebas pasan (`python -m unittest discover tests`). Se revisó con
el árbol sintáctico que todas las funciones tengan docstring, que ninguna supere las 40
líneas (la más larga tiene 26) y que el módulo no use `print()`.

**Modificaciones:** _(completar: qué cambié al leer y probar el código, y por qué.)_

**Estado:** _(completar)_
