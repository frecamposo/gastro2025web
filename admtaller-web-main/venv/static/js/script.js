// Espera a que todo el HTML esté cargado antes de intentar acceder a los elementos
document.addEventListener('DOMContentLoaded', (event) => {
    
    // Ahora sí, busca los elementos DENTRO de este bloque:
    const modal = document.getElementById("miModal");
    const btnAbrir = document.getElementById("btn-abrir-modal");
    const btnCerrar = document.getElementById("btn-cerrar-modal");

    // Verifica si encontraste los elementos (buena práctica de depuración)
    if (btnAbrir && modal && btnCerrar) {
        
        // Cuando el usuario hace clic en el botón, abre la modal
        btnAbrir.onclick = function() {
          modal.classList.add("mostrar");
        }

        // Cuando el usuario hace clic en <span> (x), cierra la modal
        btnCerrar.onclick = function() {
          modal.classList.remove("mostrar");
        }

        // Cuando el usuario hace clic en cualquier lugar fuera del contenido de la modal, la cierra
        window.onclick = function(event) {
          if (event.target == modal) {
            modal.classList.remove("mostrar");
          }
        }
    } else {
        console.error("Error: No se pudieron encontrar todos los elementos HTML necesarios.");
    }
});
