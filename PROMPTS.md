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

**Modificaciones:** El contrato se corrigió dos veces sobre la marcha. Al escribir
`main.py` aparecieron cinco cosas que faltaban (`modificar_reserva()`, `confirmar_espera()`,
`ruta_reporte()`, `fila_csv()` y la constante `RUTA_GRAFICO`) y `validar_fecha()` se partió
en dos, porque rechazaba fechas pasadas y eso rompía la búsqueda en el historial. Después
se lo pasé al equipo: Federico y Gonzalo implementaron sus módulos respetando las firmas
sin pedir cambios. Federico agregó tres funciones auxiliares internas
(`buscar_reserva_por_id()`, `es_del_turno()` y `valor_valido()`) que no estaban previstas.

**Estado:** En uso como referencia del equipo. Queda pendiente sumarle las funciones
auxiliares de Federico.

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

**Modificaciones:** No cambié el flujo generado. Lo probé contra los módulos reales
cuando Federico y Gonzalo entregaron los suyos: el menú, el despacho de opciones, el
submenú y la salida funcionan. Al ejecutarlo encontré dos cosas. Una, que el programa no
encontraba `datos/complejos.json` si se lo corría parado en otra carpeta: el problema no
estaba en `main.py` sino en las rutas relativas de `persistencia.py`, y lo corrigió
Gonzalo. La otra, que el menú se cierra solo, porque `utils.pedir_opcion()` todavía es un
stub que devuelve `"0"` sin leer el teclado.

**Estado:** En uso, sin modificaciones. Falta probarlo de punta a punta cuando esté
`utils.py`.

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

**Modificaciones:** Los stubs de `estructuras.py` y `persistencia.py` ya fueron
reemplazados por Federico y Gonzalo; los de `utils.py` y `estadisticas.py` siguen sin
implementar. El `"0"` que devuelve el stub de `pedir_opcion()` cumple su objetivo de no
dejar el menú en un bucle infinito, pero confunde al ejecutar el programa, porque parece
que se cerrara solo.

**Estado:** Cumplió su función. Se va borrando a medida que cada integrante implementa su
módulo. Queda pendiente confirmar el tipo de cancha de Golazo Fútbol, Mundial F5 y La
Bombonerita en `datos/complejos.json`.

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

---

**Fecha:** 23/09/2026 | **Herramienta:** Claude | **Integrante:** Gonzalo Tapia

**Prompt:** "Soy el encargado de persistencia" — con el enlace al repositorio y el pedido
explícito de que me explicara paso a paso en lugar de darme el código resuelto, porque
quería escribirlo yo. La IA leyó `CONTRATO_MODULOS.md` y `persistencia.py` para ver las
firmas y los `TODO [GON]`.

**Resultado:** No generó el módulo. Para cada una de las cuatro funciones me indicó qué
argumentos llevaba cada llamada y por qué, dejando huecos que completé yo: `os.makedirs()`
con `exist_ok=True`, `json.dump()` con `ensure_ascii=False` e `indent=2`, `csv.writer()`
con `writerow()` para el encabezado y `writerows()` para las filas, y `strftime()` con el
formato `"%Y-%m-%d %H:%M:%S"`. La única función que me dio armada fue `cargar_json()`,
después de pedírsela.

**Puntos que tuve que entender para escribirlo:**

- `FileNotFoundError` va antes que `OSError` en `cargar_json()`, porque es un subtipo suyo
  y Python se queda con el primer `except` que coincide. Si se invierten, el archivo nunca
  se crea.
- `newline=""` en `exportar_csv()` evita que en Windows quede una línea en blanco entre
  cada fila, porque el módulo `csv` ya escribe su propio salto.
- El log abre en modo `"a"` y no `"w"`: `"w"` vacía el archivo, así que cada operación
  borraría el historial anterior.

**Errores que encontré yo:** en `exportar_csv()` había puesto el modo `"r"` en lugar de
`"w"` y la función devolvía `0` sin explicación. Lo detecté probando la función suelta con
`python -c`, y entendí que el `except (IOError, OSError)` estaba capturando el
`FileNotFoundError` que largaba el `open()` en modo lectura.

**Verificación:** probé cada función por separado antes de commitear. El log lo corrí
cuatro veces seguidas para confirmar que el modo `"a"` acumulaba las líneas en vez de
pisarlas.

**Modificaciones:** escribí las cuatro funciones yo a partir de las indicaciones. De lo
que me pasó armado (`cargar_json`) no cambié nada, pero verifiqué el orden de los `except`
antes de aceptarlo.

**Estado:** en uso. Commits `125565d` y `4325050`.

---

**Fecha:** 28/09/2026 | **Herramienta:** Claude | **Integrante:** Gonzalo Tapia

**Prompt:** Le pasé las cinco correcciones que me hizo Leandro sobre `persistencia.py`
para ir aplicándolas una por una.

**Resultado:** El arreglo de fondo (las rutas relativas con `__file__`) no salió de la IA
sino de Leandro, que detectó que el programa creaba un `complejos.json` vacío al
ejecutarse desde otra carpeta. La IA me indicó cómo aplicarlo y qué hace `__file__`.

**Error de la IA y cómo lo resolví:** me indicó usar "Format Document" de VSCode para
normalizar la indentación. El formateador que tomó no era de Python y borró la
indentación de todo el archivo, dejándolo sin poder importarse (`IndentationError`).
Lo recuperé con `git checkout persistencia.py`, que restauró la versión del último
commit, y rehice las correcciones a mano. También me indicó un nombre mal escrito
(`_file_` con un guion bajo de cada lado en vez de `__file__` con dos), que corregí antes
de ejecutar.

**Modificaciones:** apliqué los cinco puntos a mano. Descarté rehacer el mensaje de un
commit ya subido, porque reescribir historia compartida por un error de tipeo en el
mensaje trae más problemas de los que soluciona.

**Estado:** en uso. Commit `b7026e7`.
---

**Fecha:** 29/09/2026 | **Herramienta:** Claude | **Integrante:** Gustavo Di Paola

**Prompt:** "eso tengo que hacer" — con el esqueleto de `utils.py` adjunto (firmas del
contrato y `TODO [GUS]` en cada función). La IA no tenía `CONTRATO_MODULOS.md`, así que
trabajó solo con lo que decía el archivo adjunto.

**Resultado:** Implementó las diez funciones de `utils.py` con las firmas del esqueleto,
sin cambiar ninguna: `pedir_texto()`, `pedir_entero()`, `pedir_opcion()`,
`validar_email()`, `validar_fecha()`, `validar_fecha_reserva()`, `buscar_reservas()`,
`ordenar_por()`, `formatear_reserva()` y `fila_csv()`. Agregó una función interna,
`_nombre_complejo()`, para no repetir la búsqueda del nombre del complejo en las dos
funciones de formateo.

**Decisiones de diseño que tomó y que hay que poder explicar en la defensa:**

- `validar_fecha()` exige que el texto tenga 10 caracteres antes de llamar a `strptime()`,
  porque `strptime()` acepta `2026-9-5` sin ceros y el formato pedido es `AAAA-MM-DD`.
- `validar_fecha_reserva()` reutiliza `validar_fecha()` y compara contra `date.today()`,
  así que una reserva para hoy es válida.
- `ordenar_por()` usa inserción escrita a mano, sin `sorted()`, sobre una copia de la
  lista. Es estable: dos reservas con el mismo valor conservan el orden en que venían.
- `buscar_reservas()` compara por coincidencia parcial sin distinguir mayúsculas cuando
  tanto el valor buscado como el del diccionario son texto, y por igualdad en cualquier
  otro caso (por ejemplo, un id numérico).
- `pedir_opcion()` compara como texto pero devuelve el elemento original de la lista, para
  que funcione igual con ids numéricos.

**Supuesto a confirmar:** como no tenía el contrato, la IA supuso que las reservas tienen
las claves `id_complejo` y `fecha` (formato `AAAA-MM-DD`) y que los complejos tienen `id`
y `nombre`. Esos nombres se usan solo en `formatear_reserva()`, `fila_csv()` y
`_nombre_complejo()`.

**Verificación:** la IA corrió el módulo con entrada simulada: emails como `a@b.` y
`a@@b.com`, fechas como `2026-02-30` y `2026-9-5`, reserva de ayer/hoy/mañana, lista
vacía y orden ascendente/descendente en `ordenar_por()`, y los tres pedidos por teclado
con datos inválidos antes del válido. Comprobó con el árbol sintáctico que todas las
funciones tengan docstring y que ninguna supere las 40 líneas (la más larga tiene 25).
No probó el módulo integrado con `main.py`.

**Modificaciones:** _(completar: qué cambié al leer y probar el código, y por qué. Por
ejemplo, si ajusté los nombres de las claves según `CONTRATO_MODULOS.md`.)_

**Estado:** _(completar: en uso / modificado parcialmente, y el commit donde quedó.)_


---

**Fecha:** 06/10/2026 | **Herramienta:** Claude (Claude Code) | **Integrante:** Leandro Licata

**Prompt:** "¿Qué sería la lista de espera?", después "¿Cómo se suele manejar esto? ¿Qué
es lo recomendable?" y por último "Implementalo". La pregunta surgió al probar el menú:
en la opción 1 solo se podía entrar en lista de espera cuando los cinco horarios del día
estaban ocupados, y al cancelar una reserva el turno quedaba libre hasta que alguien
entrara a la opción 5.

**Resultado:** Propuso manejar la lista de espera por horario y de forma voluntaria, como
en los sistemas de reservas reales, y reasignar el turno automáticamente al cancelar. Lo
implementó en `main.py` con tres funciones nuevas:

- `mostrar_horarios()`: imprime la grilla de horarios con libre/ocupado. La usan las
  opciones 1 y 2, así que se sacó el bucle que estaba repetido en
  `flujo_consultar_disponibilidad()`.
- `elegir_horario()`: deja elegir cualquiera de los cinco horarios. Si el elegido está
  ocupado, pregunta "¿Querés anotarte en lista de espera? (s/n)"; con "n" vuelve a pedir
  el horario. El prompt indica el formato: `Horario (HH:MM):`.
- `promover_espera()`: al cancelar, busca al primero de la cola de ese turno con
  `estructuras.siguiente_en_espera()`, lo confirma con `estructuras.confirmar_espera()`
  y lo muestra en pantalla.

`flujo_registrar_reserva()` y `flujo_cancelar_reserva()` pasaron a usar estas funciones,
y se quitó el aviso "Revisá la opción 5". La opción 5 quedó como consulta de la cola y
respaldo manual. No se tocó ningún otro módulo: todo usa funciones que ya existían en
`estructuras.py` y `utils.py`.

**Decisiones de diseño que hay que poder explicar en la defensa:**

- La cola es FIFO por turno (complejo, fecha y hora): sale primero el que se anotó
  primero, según `fecha_registro` y, si empatan, el id.
- La reasignación al cancelar se hace en `main.py` llamando a funciones de
  `estructuras.py`, sin lógica de cálculo propia, para respetar la regla de que `main.py`
  solo maneja menú y flujo.
- `confirmar_espera()` vuelve a verificar que el turno esté libre, así que nunca puede
  haber dos reservas confirmadas para el mismo turno.

**Verificación:** la IA corrió el programa sobre una copia del proyecto con datos vacíos:
reserva confirmada a las 20:00, segunda reserva para el mismo turno aceptando la lista
de espera (queda `en_espera`) y cancelación de la primera (la segunda pasa sola a
`confirmada`). Probó también entradas inválidas: horario `20`, respuesta distinta de
s/n y respuesta "n". Comprobó que ninguna función supere las 40 líneas (la más larga
tiene 29) y que los tests de `estructuras` sigan pasando.

**Modificaciones:** Probé manualmente el programa y todo funcionó correctamente, así que
no le hice cambios al código generado.

**Estado:** en uso, sin modificaciones.
