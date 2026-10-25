/* =========================================================================
   comun.js — Lo que comparten las páginas que hablan con la API del backend.
   Responsable: [LEA] Leandro Licata (Frontend / Formularios).
   -------------------------------------------------------------------------
   Lo usan reservar.js y mis-reservas.js, así no se repite en cada página.
   Se carga antes que el script de la página. El backend se levanta con
   `python api.py` y escucha en el puerto 5000.
   ------------------------------------------------------------------------- */

const API_URL = "http://localhost:5000/api";

const SIN_CONEXION = "No pudimos conectarnos con el servidor de reservas. " +
                     "Probá de nuevo en unos minutos.";


// Hace un pedido a la API y devuelve { ok, status, datos }.
// Si el servidor no está levantado, fetch lanza un error que se maneja afuera.
async function pedirApi(ruta, opciones) {
  const respuesta = await fetch(API_URL + ruta, opciones);
  const datos = await respuesta.json();
  return { ok: respuesta.ok, status: respuesta.status, datos: datos };
}


// Arma las opciones de fetch para mandar un objeto como JSON.
function enviarJson(metodo, cuerpo) {
  return {
    method: metodo,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(cuerpo)
  };
}


// Muestra un mensaje en la caja #mensaje de la página. tipo: "exito", "aviso"
// o "error". Se usa textContent (y no innerHTML) para que nada de lo que venga
// del servidor pueda inyectar HTML en la página.
function mostrarMensaje(texto, tipo) {
  const caja = document.querySelector("#mensaje");
  caja.textContent = texto;
  caja.className = "mensaje mensaje-" + tipo;
  caja.hidden = false;
}
