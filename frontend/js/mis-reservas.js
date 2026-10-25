/* =========================================================================
   mis-reservas.js — Conecta la página Mis reservas con la API del backend.
   Responsable: [LEA] Leandro Licata (Frontend / Formularios).
   -------------------------------------------------------------------------
   El cliente busca sus reservas por email, ve el detalle de una, cambia los
   jugadores o los comentarios y la cancela con un motivo. Usa los endpoints
   que ya existen en api.py, y los ids los fijó [FED] Federico en
   mis-reservas.html. Lo compartido con reservar.js (API_URL, SIN_CONEXION,
   pedirApi, enviarJson y mostrarMensaje) está en js/comun.js.
   ------------------------------------------------------------------------- */

const formBuscar       = document.querySelector("#form-buscar");
const inputEmail       = document.querySelector("#buscar-email");
const botonBuscar      = formBuscar.querySelector('button[type="submit"]');
const resultados       = document.querySelector("#resultados");
const listaReservas    = document.querySelector("#lista-reservas");
const sinResultados    = document.querySelector("#sin-resultados");
const detalle          = document.querySelector("#detalle");
const formJugadores    = document.querySelector("#form-jugadores");
const inputJugadores   = document.querySelector("#nuevos-jugadores");
const formComentarios  = document.querySelector("#form-comentarios");
const inputComentarios = document.querySelector("#nuevos-comentarios");
const formCancelar     = document.querySelector("#form-cancelar");
const inputMotivo      = document.querySelector("#motivo");
const botonVolver      = document.querySelector("#volver-listado");

const TEXTO_ESTADO = {
  confirmada: "Confirmada",
  en_espera:  "En lista de espera",
  cancelada:  "Cancelada"
};

let nombresComplejos = {};   // id del complejo -> nombre, desde GET /api/complejos
let emailBuscado = "";       // para volver a buscar al regresar del detalle
let reservaActual = null;    // la reserva que se está viendo en el detalle


// 1) Carga los nombres de los complejos, para mostrar "Estadio 5" y no el id.
async function cargarComplejos() {
  try {
    const { datos } = await pedirApi("/complejos");
    for (const complejo of datos) {
      nombresComplejos[complejo.id] = complejo.nombre;
    }
  } catch (error) {
    botonBuscar.disabled = true;
    mostrarMensaje(SIN_CONEXION, "error");
  }
}


// 2) Pasa una fecha AAAA-MM-DD al formato DD/MM/AAAA que se usa en el sitio.
function formatearFecha(fecha) {
  const [anio, mes, dia] = fecha.split("-");
  return dia + "/" + mes + "/" + anio;
}


// 3) Arma el <li> de una reserva del listado, con su botón "Ver detalle".
//    El id va en data-id: un solo listener en la lista atiende todos los botones.
function crearItem(reserva) {
  const item = document.createElement("li");
  item.className = "item-reserva";
  const texto = document.createElement("span");
  texto.textContent = "#" + reserva.id + " · " + nombresComplejos[reserva.id_complejo] +
                      " · " + formatearFecha(reserva.fecha) + " " + reserva.hora +
                      " · " + TEXTO_ESTADO[reserva.estado];
  const boton = document.createElement("button");
  boton.type = "button";
  boton.className = "boton boton-secundario";
  boton.textContent = "Ver detalle";
  boton.dataset.id = reserva.id;
  item.append(texto, boton);
  return item;
}


// 4) Busca las reservas de un email con GET /api/reservas y arma el listado.
//    La API busca por coincidencia parcial ("ana@" encontraría a "mariana@..."),
//    así que acá se dejan solo las de email exacto: cada cliente ve las suyas.
async function buscarReservas(email) {
  const ruta = "/reservas?campo=email&valor=" + encodeURIComponent(email);
  try {
    const { ok, datos } = await pedirApi(ruta);
    if (!ok) return mostrarMensaje(datos.error, "error");
    const propias = datos.filter((reserva) => reserva.email.toLowerCase() === email);
    listaReservas.replaceChildren(...propias.map(crearItem));
    sinResultados.hidden = propias.length > 0;
    detalle.hidden = true;
    resultados.hidden = false;
  } catch (error) {
    mostrarMensaje(SIN_CONEXION, "error");
  }
}


// 5) Muestra el detalle de una reserva. Si está cancelada, se ocultan las
//    acciones: la API ya no deja modificarla ni volver a cancelarla.
function mostrarDetalle(reserva) {
  reservaActual = reserva;
  document.querySelector("#detalle-id").textContent = "#" + reserva.id;
  document.querySelector("#detalle-complejo").textContent = nombresComplejos[reserva.id_complejo];
  document.querySelector("#detalle-fecha").textContent = formatearFecha(reserva.fecha);
  document.querySelector("#detalle-hora").textContent = reserva.hora;
  document.querySelector("#detalle-jugadores").textContent = reserva.jugadores;
  document.querySelector("#detalle-comentarios").textContent = reserva.comentarios || "—";
  const estado = TEXTO_ESTADO[reserva.estado];
  document.querySelector("#detalle-estado").textContent = reserva.motivo_cancelacion
    ? estado + " (motivo: " + reserva.motivo_cancelacion + ")" : estado;
  inputJugadores.value = reserva.jugadores;
  inputComentarios.value = reserva.comentarios;
  inputMotivo.value = "";
  const cancelada = reserva.estado === "cancelada";
  formJugadores.hidden = cancelada;
  formComentarios.hidden = cancelada;
  formCancelar.hidden = cancelada;
  resultados.hidden = true;
  detalle.hidden = false;
}


// 6) Pide una reserva con GET /api/reservas/<id>, para mostrarla actualizada.
async function verDetalle(id) {
  try {
    const { ok, datos } = await pedirApi("/reservas/" + id);
    if (!ok) return mostrarMensaje(datos.error, "error");
    document.querySelector("#mensaje").hidden = true;
    mostrarDetalle(datos);
  } catch (error) {
    mostrarMensaje(SIN_CONEXION, "error");
  }
}


// 7) Cambia los jugadores o los comentarios con PATCH /api/reservas/<id>.
//    jugadores va como número: la API rechaza "10" como texto.
async function modificar(campo, valor) {
  try {
    const { ok, datos } = await pedirApi("/reservas/" + reservaActual.id,
                                         enviarJson("PATCH", { campo: campo, valor: valor }));
    if (!ok) return mostrarMensaje(datos.error, "error");
    mostrarDetalle(datos);
    mostrarMensaje("Listo: se guardaron los cambios de la reserva #" + datos.id + ".", "exito");
  } catch (error) {
    mostrarMensaje(SIN_CONEXION, "error");
  }
}


// 8) Cancela con POST /api/reservas/<id>/cancelar. Si había alguien en la lista
//    de espera, la API le pasa el turno; acá no se muestra quién es, porque son
//    los datos de otro cliente.
async function cancelar(motivo) {
  try {
    const { ok, datos } = await pedirApi("/reservas/" + reservaActual.id + "/cancelar",
                                         enviarJson("POST", { motivo: motivo }));
    if (!ok) return mostrarMensaje(datos.error, "error");
    mostrarDetalle(datos.reserva);
    const aviso = datos.promovida ? " El turno pasó al primero de la lista de espera." : "";
    mostrarMensaje("La reserva #" + datos.reserva.id + " quedó cancelada." + aviso, "exito");
  } catch (error) {
    mostrarMensaje(SIN_CONEXION, "error");
  }
}


// 9) Conexión de los eventos y carga inicial. Cada submit hace preventDefault:
//    los formularios no se envían solos, el pedido lo hace fetch.
formBuscar.addEventListener("submit", (evento) => {
  evento.preventDefault();
  emailBuscado = inputEmail.value.trim().toLowerCase();
  document.querySelector("#mensaje").hidden = true;
  buscarReservas(emailBuscado);
});
listaReservas.addEventListener("click", (evento) => {
  const boton = evento.target.closest("button[data-id]");
  if (boton) verDetalle(boton.dataset.id);
});
formJugadores.addEventListener("submit", (evento) => {
  evento.preventDefault();
  modificar("jugadores", Number(inputJugadores.value));
});
formComentarios.addEventListener("submit", (evento) => {
  evento.preventDefault();
  modificar("comentarios", inputComentarios.value.trim());
});
formCancelar.addEventListener("submit", (evento) => {
  evento.preventDefault();
  cancelar(inputMotivo.value.trim());
});
botonVolver.addEventListener("click", () => {
  document.querySelector("#mensaje").hidden = true;
  buscarReservas(emailBuscado);
});
cargarComplejos();
