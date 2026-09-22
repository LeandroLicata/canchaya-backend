# main.py — Punto de entrada del backend de CanchaYa.
# [LEA] Leandro Licata — menú, flujo e integración de módulos.
#
# Este módulo NO contiene lógica de cálculo ni define estructuras de datos: solo muestra
# el menú, pide los datos con utils y delega el trabajo en los demás módulos. Es el único
# módulo que imprime en pantalla (ver CONTRATO_MODULOS.md).

import estadisticas
import estructuras
import persistencia
import utils

OPCIONES_MENU = ("1", "2", "3", "4", "5", "6", "7", "0")
MIN_JUGADORES = 2
MAX_JUGADORES = 14


def mostrar_menu():
    """Imprime el menú principal. No recibe parámetros ni devuelve nada."""
    print("\n" + "=" * 52)
    print("  CanchaYa — Gestión de reservas")
    print("=" * 52)
    print("  1. Registrar una reserva")
    print("  2. Consultar disponibilidad")
    print("  3. Consultas y búsquedas")
    print("  4. Modificar o cancelar una reserva")
    print("  5. Lista de espera")
    print("  6. Estadísticas del período")
    print("  7. Exportar reporte diario a CSV")
    print("  0. Salir")


def mostrar_submenu_consultas():
    """Imprime el submenú de búsquedas. No recibe parámetros ni devuelve nada."""
    print("\n  1. Buscar por cliente (nombre o email)")
    print("  2. Buscar por complejo")
    print("  3. Buscar por fecha")


def pedir_validado(mensaje, validador, error, largo_minimo=1):
    """Pide un texto y lo reintenta hasta que la función validadora lo acepte.

    Parámetros:
        mensaje: texto que se le muestra al usuario.
        validador: función de utils que recibe el texto y devuelve True o False.
        error: mensaje a mostrar cuando el dato no es válido.
        largo_minimo: largo mínimo exigido al texto (por defecto 1).
    Devuelve:
        El texto ya validado.
    """
    texto = utils.pedir_texto(mensaje, largo_minimo)
    while not validador(texto):
        print("  " + error)
        texto = utils.pedir_texto(mensaje, largo_minimo)
    return texto


def elegir_complejo(lista_complejos):
    """Muestra los complejos disponibles y devuelve el diccionario del elegido.

    Parámetros: la lista de complejos cargada desde el JSON.
    Devuelve: el diccionario del complejo seleccionado.
    """
    print("\n  Complejos disponibles:")
    for complejo in lista_complejos:
        print("   {0}. {1} ({2}) — $ {3} / hora".format(
            complejo["id"], complejo["nombre"], complejo["zona"], complejo["precio_hora"]))
    ids = [complejo["id"] for complejo in lista_complejos]
    id_elegido = utils.pedir_opcion("  Número de complejo: ", ids)
    # pedir_opcion solo devuelve un id de la lista, así que el for siempre encuentra uno.
    for complejo in lista_complejos:
        if complejo["id"] == id_elegido:
            return complejo


def mostrar_reservas(reservas, lista_complejos, titulo="Resultados"):
    """Imprime una lista de reservas ordenada por fecha.

    Parámetros: las reservas a mostrar, los complejos y el título del listado.
    Devuelve: nada.
    """
    if not reservas:
        print("  No se encontraron reservas.")
        return
    ordenadas = utils.ordenar_por(reservas, "fecha")
    print("\n  {0} ({1}):".format(titulo, len(ordenadas)))
    for reserva in ordenadas:
        print("   " + utils.formatear_reserva(reserva, lista_complejos))


def elegir_reserva(lista_reservas, lista_complejos, accion):
    """Muestra las reservas confirmadas y devuelve el id de la elegida.

    Parámetros: la lista de reservas, la de complejos y el verbo de la acción.
    Devuelve: el id elegido, o None si no hay reservas confirmadas.
    """
    activas = utils.buscar_reservas(lista_reservas, "estado", "confirmada")
    if not activas:
        print("  No hay reservas confirmadas.")
        return None
    mostrar_reservas(activas, lista_complejos, "Reservas confirmadas")
    ids = [reserva["id"] for reserva in activas]
    return utils.pedir_opcion("  Número de reserva a {0}: ".format(accion), ids)


def flujo_registrar_reserva(lista_reservas, lista_complejos):
    """Pide los datos de una reserva nueva y la agrega.

    Parámetros: la lista de reservas y la de complejos.
    Devuelve: la lista de reservas actualizada.
    """
    complejo = elegir_complejo(lista_complejos)
    fecha = pedir_validado("  Fecha (AAAA-MM-DD): ", utils.validar_fecha_reserva,
                           "Fecha inválida o ya pasada.")
    libres = estructuras.horarios_disponibles(lista_reservas, complejo["id"], fecha)
    if libres:
        hora = utils.pedir_opcion("  Horario: ", libres)
    else:
        print("  No quedan horarios libres para esa fecha: vas a entrar en lista de espera.")
        hora = utils.pedir_opcion("  Horario deseado: ", list(estructuras.HORARIOS))

    datos = {
        "nombre_cliente": utils.pedir_texto("  Nombre y apellido: ", 3),
        "email": pedir_validado("  Email: ", utils.validar_email, "Email inválido.", 5),
        "telefono": utils.pedir_texto("  Teléfono: ", 6),
        "id_complejo": complejo["id"],
        "fecha": fecha,
        "hora": hora,
        "jugadores": utils.pedir_entero("  Cantidad de jugadores: ",
                                        MIN_JUGADORES, MAX_JUGADORES),
        "comentarios": utils.pedir_texto("  Comentarios (opcional): ", 0),
    }
    reserva = estructuras.crear_reserva(lista_reservas, datos)
    lista_reservas, estado = estructuras.agregar_reserva(lista_reservas, reserva)
    print("\n  Reserva #{0} registrada — estado: {1}.".format(reserva["id"], estado))
    persistencia.registrar_log("registrar_reserva", "#{0} {1}".format(reserva["id"], estado))
    return lista_reservas


def flujo_consultar_disponibilidad(lista_reservas, lista_complejos):
    """Muestra los horarios libres y ocupados de un complejo en una fecha.

    Parámetros: la lista de reservas y la de complejos.
    Devuelve: nada.
    """
    complejo = elegir_complejo(lista_complejos)
    fecha = pedir_validado("  Fecha (AAAA-MM-DD): ", utils.validar_fecha, "Fecha inválida.")
    libres = estructuras.horarios_disponibles(lista_reservas, complejo["id"], fecha)
    print("\n  {0} — {1}".format(complejo["nombre"], fecha))
    for hora in estructuras.HORARIOS:
        if hora in libres:
            print("   {0}   libre".format(hora))
        else:
            print("   {0}   ocupado".format(hora))
    persistencia.registrar_log("consultar_disponibilidad",
                               "{0} {1}".format(complejo["nombre"], fecha))


def flujo_consultas(lista_reservas, lista_complejos):
    """Submenú de búsquedas: por cliente, por complejo o por fecha.

    Parámetros: la lista de reservas y la de complejos.
    Devuelve: nada.
    """
    mostrar_submenu_consultas()
    opcion = utils.pedir_opcion("  Elegí una búsqueda: ", ["1", "2", "3"])
    if opcion == "1":
        valor = utils.pedir_texto("  Nombre o email del cliente: ", 3)
        encontradas = utils.buscar_reservas(lista_reservas, "nombre_cliente", valor)
        encontradas = encontradas + utils.buscar_reservas(lista_reservas, "email", valor)
    elif opcion == "2":
        complejo = elegir_complejo(lista_complejos)
        encontradas = utils.buscar_reservas(lista_reservas, "id_complejo", complejo["id"])
    else:
        fecha = pedir_validado("  Fecha (AAAA-MM-DD): ", utils.validar_fecha,
                               "Fecha inválida.")
        encontradas = utils.buscar_reservas(lista_reservas, "fecha", fecha)
    mostrar_reservas(encontradas, lista_complejos)
    persistencia.registrar_log("buscar_reservas",
                               "{0} resultados".format(len(encontradas)))


def flujo_modificar_reserva(lista_reservas, lista_complejos):
    """Modifica la cantidad de jugadores o los comentarios de una reserva.

    Parámetros: la lista de reservas y la de complejos.
    Devuelve: la lista de reservas actualizada.
    """
    id_reserva = elegir_reserva(lista_reservas, lista_complejos, "modificar")
    if id_reserva is None:
        return lista_reservas
    campo = utils.pedir_opcion("  ¿Qué querés modificar? (jugadores / comentarios): ",
                               ["jugadores", "comentarios"])
    if campo == "jugadores":
        valor = utils.pedir_entero("  Nueva cantidad: ", MIN_JUGADORES, MAX_JUGADORES)
    else:
        valor = utils.pedir_texto("  Nuevos comentarios: ", 0)
    lista_reservas, modificada = estructuras.modificar_reserva(
        lista_reservas, id_reserva, campo, valor)
    if modificada:
        print("  Reserva actualizada.")
        persistencia.registrar_log("modificar_reserva",
                                   "#{0} {1}".format(id_reserva, campo))
    else:
        print("  No se pudo modificar la reserva.")
    return lista_reservas


def flujo_cancelar_reserva(lista_reservas, lista_complejos):
    """Cancela una reserva y avisa si hay alguien esperando ese turno.

    Parámetros: la lista de reservas y la de complejos.
    Devuelve: la lista de reservas actualizada.
    """
    id_reserva = elegir_reserva(lista_reservas, lista_complejos, "cancelar")
    if id_reserva is None:
        return lista_reservas
    motivo = utils.pedir_texto("  Motivo de la cancelación: ", 3)
    lista_reservas, cancelada = estructuras.cancelar_reserva(
        lista_reservas, id_reserva, motivo)
    if not cancelada:
        print("  No se pudo cancelar la reserva.")
        return lista_reservas
    print("  Reserva #{0} cancelada.".format(id_reserva))
    persistencia.registrar_log("cancelar_reserva", "#{0} {1}".format(id_reserva, motivo))
    print("  Revisá la opción 5 por si alguien está esperando ese turno.")
    return lista_reservas


def flujo_modificar_cancelar(lista_reservas, lista_complejos):
    """Pregunta si se quiere modificar o cancelar y deriva al flujo que corresponde.

    Parámetros: la lista de reservas y la de complejos.
    Devuelve: la lista de reservas actualizada.
    """
    print("\n  1. Modificar una reserva")
    print("  2. Cancelar una reserva")
    opcion = utils.pedir_opcion("  Elegí una acción: ", ["1", "2"])
    if opcion == "1":
        return flujo_modificar_reserva(lista_reservas, lista_complejos)
    return flujo_cancelar_reserva(lista_reservas, lista_complejos)


def flujo_lista_espera(lista_reservas, lista_complejos):
    """Muestra el primero de la cola de un turno y lo confirma si el turno se liberó.

    Parámetros: la lista de reservas y la de complejos.
    Devuelve: la lista de reservas actualizada.
    """
    complejo = elegir_complejo(lista_complejos)
    fecha = pedir_validado("  Fecha (AAAA-MM-DD): ", utils.validar_fecha, "Fecha inválida.")
    hora = utils.pedir_opcion("  Horario: ", list(estructuras.HORARIOS))
    siguiente = estructuras.siguiente_en_espera(lista_reservas, complejo["id"], fecha, hora)
    if siguiente is None:
        print("  No hay nadie en lista de espera para ese turno.")
        return lista_reservas
    print("\n  Primero en la cola:")
    print("   " + utils.formatear_reserva(siguiente, lista_complejos))
    if estructuras.esta_ocupado(lista_reservas, complejo["id"], fecha, hora):
        print("  El turno sigue ocupado: todavía no se le puede confirmar.")
        return lista_reservas
    lista_reservas, confirmada = estructuras.confirmar_espera(lista_reservas,
                                                              siguiente["id"])
    if confirmada:
        print("  Turno confirmado para la reserva #{0}.".format(siguiente["id"]))
        persistencia.registrar_log("confirmar_espera", "#{0}".format(siguiente["id"]))
    else:
        print("  No se pudo confirmar la reserva.")
    return lista_reservas


def flujo_estadisticas(lista_reservas, lista_complejos):
    """Muestra las estadísticas del período y genera el gráfico de ocupación.

    Parámetros: la lista de reservas y la de complejos.
    Devuelve: nada.
    """
    if not lista_reservas:
        print("  Todavía no hay reservas cargadas.")
        return
    ocupacion = estadisticas.ocupacion_por_horario(lista_reservas)
    ingresos = estadisticas.ingresos_por_complejo(lista_reservas, lista_complejos)
    ranking = estadisticas.ranking_complejos(lista_reservas, lista_complejos)
    canceladas = estadisticas.porcentaje_cancelaciones(lista_reservas)

    print("\n  Ocupación por horario:")
    for hora in estructuras.HORARIOS:
        cantidad = ocupacion.get(hora, 0)
        print("   {0}   {1} ({2})".format(hora, "#" * cantidad, cantidad))
    print("\n  Ingresos por complejo:")
    for nombre in ingresos:
        print("   {0}: $ {1}".format(nombre, ingresos[nombre]))
    print("\n  Complejos más reservados:")
    for puesto, (nombre, cantidad) in enumerate(ranking, start=1):
        print("   {0}. {1} ({2} reservas)".format(puesto, nombre, cantidad))
    print("\n  Reservas canceladas: {0} %".format(canceladas))

    if estadisticas.graficar_ocupacion(ocupacion, persistencia.RUTA_GRAFICO):
        print("  Gráfico guardado en {0}".format(persistencia.RUTA_GRAFICO))
    persistencia.registrar_log("ver_estadisticas", "{0} reservas".format(len(lista_reservas)))


def flujo_exportar_csv(lista_reservas, lista_complejos):
    """Exporta a CSV las reservas de una fecha.

    Parámetros: la lista de reservas y la de complejos.
    Devuelve: nada.
    """
    fecha = pedir_validado("  Fecha del reporte (AAAA-MM-DD): ", utils.validar_fecha,
                           "Fecha inválida.")
    del_dia = utils.buscar_reservas(lista_reservas, "fecha", fecha)
    if not del_dia:
        print("  No hay reservas para esa fecha.")
        return
    encabezados = ["id", "cliente", "email", "telefono", "complejo",
                   "hora", "jugadores", "estado"]
    filas = [utils.fila_csv(reserva, lista_complejos)
             for reserva in utils.ordenar_por(del_dia, "hora")]
    ruta = persistencia.ruta_reporte(fecha)
    escritas = persistencia.exportar_csv(ruta, encabezados, filas)
    if escritas > 0:
        print("  {0} reservas exportadas a {1}".format(escritas, ruta))
    else:
        print("  No se pudo generar el reporte.")
    persistencia.registrar_log("exportar_csv", "{0} filas".format(escritas))


def ejecutar_opcion(opcion, lista_reservas, lista_complejos):
    """Ejecuta el flujo que corresponde a la opción elegida en el menú.

    Parámetros: la opción elegida, la lista de reservas y la de complejos.
    Devuelve: la lista de reservas, actualizada si la opción la modificó.
    """
    if opcion == "1":
        lista_reservas = flujo_registrar_reserva(lista_reservas, lista_complejos)
    elif opcion == "2":
        flujo_consultar_disponibilidad(lista_reservas, lista_complejos)
    elif opcion == "3":
        flujo_consultas(lista_reservas, lista_complejos)
    elif opcion == "4":
        lista_reservas = flujo_modificar_cancelar(lista_reservas, lista_complejos)
    elif opcion == "5":
        lista_reservas = flujo_lista_espera(lista_reservas, lista_complejos)
    elif opcion == "6":
        flujo_estadisticas(lista_reservas, lista_complejos)
    elif opcion == "7":
        flujo_exportar_csv(lista_reservas, lista_complejos)
    return lista_reservas


def main():
    """Carga los datos, ejecuta el bucle del menú y guarda al salir.

    No recibe parámetros ni devuelve nada.
    """
    lista_complejos = persistencia.cargar_json(persistencia.RUTA_COMPLEJOS, [])
    lista_reservas = persistencia.cargar_json(persistencia.RUTA_RESERVAS, [])
    persistencia.registrar_log("inicio", "{0} reservas cargadas".format(len(lista_reservas)))

    if not lista_complejos:
        print("No hay complejos cargados. Revisá {0}.".format(persistencia.RUTA_COMPLEJOS))
        return

    opcion = ""
    while opcion != "0":
        mostrar_menu()
        opcion = utils.pedir_opcion("  Opción: ", list(OPCIONES_MENU))
        if opcion != "0":
            lista_reservas = ejecutar_opcion(opcion, lista_reservas, lista_complejos)
            # Se guarda después de cada operación y no solo al salir, para no perder
            # datos si el programa se corta de forma inesperada.
            persistencia.guardar_json(persistencia.RUTA_RESERVAS, lista_reservas)

    persistencia.registrar_log("cierre", "{0} reservas guardadas".format(len(lista_reservas)))
    print("\n  Hasta luego.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Ctrl+C no debe dejar un traceback en pantalla: se corta de forma prolija.
        print("\n\n  Sesión interrumpida por el usuario.\n")
