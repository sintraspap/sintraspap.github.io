// ---------- Buscador (Empresas) ----------
function filtrarDirectorio(){
  const q = (document.getElementById('q')?.value || '').toLowerCase();
  document.querySelectorAll('#tabla-empresas tbody tr').forEach(tr=>{
    tr.style.display = tr.innerText.toLowerCase().includes(q) ? '' : 'none';
  });
}
// Hacemos que la función sea global para que funcione con oninput
window.filtrarDirectorio = filtrarDirectorio;

// ---------- Cargar empresas desde un archivo JSON ----------
async function cargarEmpresasDesdeJSON() {
  const tablaBody = document.querySelector('#tabla-empresas tbody');
  if (!tablaBody) return;

  try {
    // Mostrar mensaje de carga mientras se obtienen los datos
    tablaBody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 20px;">Cargando empresas...</td></tr>';

    // 1. Obtener los datos del archivo JSON
    // Se usa la ruta absoluta desde la raíz del sitio para evitar problemas de rutas relativas
   const response = await fetch("/data/empresas.json");
    if (!response.ok) {
      throw new Error(`Error al cargar el archivo JSON: ${response.status} ${response.statusText}`);
    }
    const empresas = await response.json();

    // 2. Limpiar el contenido de la tabla (eliminar mensaje de carga)
    tablaBody.innerHTML = '';

    // 3. Generar las filas HTML a partir de los datos JSON
    if (empresas && empresas.length > 0) {
      empresas.forEach(empresa => {
        const fila = document.createElement('tr');
        
        // Los datos del JSON ya vienen limpios, pero se mantiene la limpieza por si acaso
        let rubroLimpio = empresa.rubro || '';
        // Quitar punto y coma inicial o final y espacios
        rubroLimpio = rubroLimpio.replace(/^\s*;+|;+\s*$/g, '');
        // Separar por punto y coma, limpiar espacios, filtrar vacíos y unir con coma y espacio
        rubroLimpio = rubroLimpio
          .split(';')
          .map(r => r.trim())
          .filter(Boolean)
          .join(', ');

        fila.innerHTML = `
          <td>${empresa.id || ''}</td>
          <td>${empresa.empresa || ''}</td>
          <td>${empresa.resolucion || ''}</td>
          <td>${empresa.fecha || ''}</td>
          <td>${rubroLimpio}</td>
        `;
        tablaBody.appendChild(fila);
      });
    } else {
      // Si el JSON está vacío o no tiene empresas
      tablaBody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 20px;">No se encontraron empresas.</td></tr>';
    }

  } catch (error) {
    console.error("Error al cargar o procesar las empresas:", error);
    tablaBody.innerHTML = `<tr><td colspan="5" style="text-align: center; padding: 20px; color: red;">Error al cargar la lista de empresas: ${error.message}</td></tr>`;
  }
}

// ---------- Agregar columna Estado (como hacía el script original) ----------
function agregarEstadoYLimpiarRubros(){
  const table = document.getElementById('tabla-empresas');
  if (!table) return;

  // 1) Agregar <th> "Estado" antes de "Rubro" si no existe
  const headRow = table.tHead && table.tHead.rows[0];
  if (headRow) {
    const ths = Array.from(headRow.cells);
    const yaTieneEstado = ths.some(th => th.textContent.trim().toLowerCase() === 'estado');
    if (!yaTieneEstado) {
      const thRubro = ths.find(th => th.textContent.trim().toLowerCase() === 'rubro');
      const thEstado = document.createElement('th');
      thEstado.textContent = 'Estado';
      if (thRubro) headRow.insertBefore(thEstado, thRubro);
      else headRow.appendChild(thEstado);
    }
  }

  // 2) En cada fila, insertar <td>Habilitado antes del Rubro si no existe
  const tbody = table.tBodies[0];
  if (!tbody) return;

  Array.from(tbody.rows).forEach(tr => {
    const celdas = Array.from(tr.cells);
    const idxRubro = celdas.length - 1; // la última celda es "Rubro"
    const yaTieneEstado = celdas.some(td => td.dataset && td.dataset.col === 'estado');

    if (!yaTieneEstado) {
      const tdEstado = document.createElement('td');
      tdEstado.textContent = 'Habilitado';
      tdEstado.dataset.col = 'estado';
      if (idxRubro >= 0) tr.insertBefore(tdEstado, celdas[idxRubro]);
      else tr.appendChild(tdEstado);
    }

    // 3) Limpiar el texto del "Rubro" (quitar ;;; y espacios)
    // ESTO YA LO HACE cargarEmpresasDesdeJSON, pero lo dejamos por si acaso
    const rubroTd = tr.lastElementChild;
    if (rubroTd && (!rubroTd.dataset || rubroTd.dataset.col !== 'estado')) {
      let txt = rubroTd.textContent || '';
      txt = txt.replace(/^\s*;+|;+\s*$/g, '');
      txt = txt
        .split(';')
        .map(r => r.trim())
        .filter(Boolean)
        .join(', ');
      rubroTd.textContent = txt;
    }
  });
}

// ---------- Inicialización cuando se carga la página ----------
window.addEventListener('DOMContentLoaded', async () => {
  await cargarEmpresasDesdeJSON(); // Cargar y mostrar las empresas
  agregarEstadoYLimpiarRubros();  // Agregar columna Estado y limpiar rubros
});
