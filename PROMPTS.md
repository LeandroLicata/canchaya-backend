# Registro de uso de IA

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

**Fecha:** 15/09/2026 | **Herramienta:** Claude (Claude Code) | **Integrante:** Leandro Licata

**Prompt:** "Hacé la documentación que hay que entregar para el Hito 0" y, a continuación,
"tiene que ser un documento para entregar en Word o PDF según lo que dice la consigna".

**Resultado:** Primero generó el pitch en markdown. Después armó el documento de entrega
con la biblioteca `python-docx` y lo exportó a PDF desde Word: encabezado institucional,
tabla de integrantes con responsabilidades, tema, alcance funcional, diseño técnico, eje
de investigación, plan de trabajo y trazabilidad, todo en una sola página.

**Errores y correcciones durante el trabajo:** (a) la URL del repositorio había quedado en
gris de 8 pt y como texto plano, perdida al final de un renglón; se rehízo como
hipervínculo real y más visible, y al agregar ese renglón el documento se pasó a dos
páginas, por lo que hubo que compactar el espaciado de los títulos para volver a una;
(b) la docente avisó que el video tutorial no se va a tomar y se quitó del plan de
trabajo, aunque la consigna lo siga listando.

**Modificaciones:** La IA eligió por su cuenta el eje de investigación (Opción D,
matplotlib); el equipo revisó esa decisión y la mantuvo. Se decidió además no versionar el
documento en el repositorio, porque la entrega va por la plataforma del instituto, y
dejar el repo solo con código y documentación de código.

**Estado:** Documento modificado varias veces antes de la entrega.

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
