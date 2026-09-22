# CLAUDE.md

Backend de CanchaYa — Proyecto Integrador de Programación I, equipo **Zonda Bytes**.
Aplicación de consola en Python, sin framework.

Las firmas de todas las funciones están en `CONTRATO_MODULOS.md`: esa es la fuente de
verdad. Este archivo solo fija las reglas, no las repite.

## Restricciones de la consigna (no negociables)

- Programación estructurada: **sin clases ni POO**. Las entidades son diccionarios dentro
  de listas, armados por funciones constructoras `crear_*()`.
- `snake_case` en variables, funciones, módulos y claves de diccionarios. Nunca camelCase
  ni PascalCase, tampoco en las claves del JSON.
- Ninguna función supera las **40 líneas** de código.
- **Toda función lleva docstring** con qué hace, qué recibe y qué devuelve.
- `try/except` en las operaciones de archivo (`FileNotFoundError`, `IOError`) y en las
  conversiones de tipo (`ValueError`). El programa no falla si un archivo no existe al
  iniciar: lo crea vacío o con valores por defecto.
- Toda entrada del usuario se valida con bucle de reintento y mensaje claro. El programa
  no debe cortarse nunca por un dato mal ingresado.
- Sin código duplicado, sin imports sin usar y sin funciones que nunca se llamen.
- Cada `.py` empieza con un comentario que indica su propósito y la sigla del responsable.

## Reglas de este proyecto

- **Solo `main.py` imprime en pantalla.** Los demás módulos calculan y devuelven valores;
  la única excepción son las funciones `pedir_*()` de `utils.py`. Es lo que permite reusar
  la misma lógica desde la API con Flask sin tocar nada.
- **`main.py` no tiene lógica de cálculo ni define estructuras de datos**: solo menú, flujo
  y llamadas a los demás módulos.
- Importar con `import persistencia` y llamar `persistencia.cargar_json(...)`.
  Nunca `from ... import *`.
- Los ordenamientos se hacen con algoritmo propio de inserción, no con `sorted()`.
- Las rutas de archivos viven en `persistencia.py`; la constante `HORARIOS`, en
  `estructuras.py`.

## Autoría por módulo

| Módulo | Responsable |
|---|---|
| `main.py` | Leandro Licata |
| `estructuras.py` | Federico Cabrera |
| `persistencia.py` | Gonzalo Tapia |
| `utils.py` y `estadisticas.py` | Gustavo Di Paola |

**No implementar los módulos de otros integrantes.** La defensa oral es individual y cada
uno responde por el código que figura bajo sus commits. Si hace falta una función de otro
módulo, dejar el stub con la firma, el docstring y un `# TODO [SIGLA]`, nunca el código
resuelto.

## Commits

- Mensajes en español, descriptivos, que digan qué cambió y por qué.
- **Sin firma ni atribución de Claude ni de Anthropic.**
- Incrementales: deben reflejar avance real, no subidas masivas al final.

## Uso de IA

Todo uso significativo de IA se registra en `PROMPTS.md` con fecha, herramienta, prompt,
resultado, modificaciones aplicadas por el integrante y estado final del código. Los
campos de modificaciones los completa la persona, no la IA.
