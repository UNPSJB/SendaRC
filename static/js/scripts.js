function initializeDataTable(selector) {
  return $(selector).DataTable({
      "destroy": true,
      pageLength: 10,
      lengthChange: false,
      columnDefs: [{ orderable: false, targets: -1 }],
      language: {
          decimal: ",",
          thousands: ".",
          processing: "Procesando...",
          search: "Buscar:",
          lengthMenu: "Mostrar _MENU_ registros",
          info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
          infoEmpty: "Mostrando 0 a 0 de 0 registros",
          infoFiltered: "(filtrado de _MAX_ registros totales)",
          infoPostFix: "",
          loadingRecords: "Cargando...",
          zeroRecords: "No se encontraron registros coincidentes",
          emptyTable: "No hay datos disponibles en la tabla",
          paginate: {
              previous: "Anterior",
              next: "Siguiente",
          },
          aria: {
              sortAscending: ": activar para ordenar la columna de manera ascendente",
              sortDescending: ": activar para ordenar la columna de manera descendente"
          }
      },
      order: [[0, "desc"]],
  });
}

function setupDataTableFilters(tableSelector, formSelector, resultSelector) {
  $(formSelector).on('change', 'select, input, input[type="date"]', function () {
      $.ajax({
          url: $(formSelector).attr('action'),
          data: $(formSelector).serialize(),
          success: function (response) {
              if ($.fn.DataTable.isDataTable(tableSelector)) {
                  $(tableSelector).DataTable().destroy();
              }

              $(resultSelector).html(response.html);

              initializeDataTable(tableSelector);
          }
      });
  });
}



$(function () {
  $("#offcanvasExample").on("show.bs.offcanvas", function (event) {
    var button = $(event.relatedTarget);
    var url = button.data("url");
    var modal = $(this);
    modal.find(".offcanvas-body").load(url);
  });
});


document.addEventListener('DOMContentLoaded', function() {
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
});

// Funcionalidad de sidebar responsive
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si estamos en la página de login
    const isLoginPage = document.querySelector('.login-container') !== null;
    
    // No crear el botón hamburger si estamos en login
    if (isLoginPage) {
        return;
    }
    
    // Crear el botón hamburger
    const mobileToggle = document.createElement('button');
    mobileToggle.className = 'mobile-menu-toggle';
    mobileToggle.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
    `;
    
    // Crear el overlay
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    
    // Insertar elementos en el DOM
    document.body.appendChild(mobileToggle);
    document.body.appendChild(overlay);
    
    const sidebar = document.getElementById('sidebar');
    
    // Solo continuar si existe la sidebar
    if (!sidebar) {
        return;
    }
    
    // Función para abrir sidebar
    function openSidebar() {
        sidebar.classList.add('active');
        overlay.classList.add('active');
        document.body.classList.add('sidebar-open');
        
        // Cambiar icono a X
        mobileToggle.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        `;
    }
    
    // Función para cerrar sidebar
    function closeSidebar() {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
        document.body.classList.remove('sidebar-open');
        
        // Cambiar icono a hamburger
        mobileToggle.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <line x1="3" y1="12" x2="21" y2="12"></line>
                <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
        `;
    }
    
    // Toggle sidebar
    function toggleSidebar() {
        if (sidebar.classList.contains('active')) {
            closeSidebar();
        } else {
            openSidebar();
        }
    }
    
    // Event listeners
    mobileToggle.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', closeSidebar);
    
    // Cerrar sidebar al hacer clic en un enlace (opcional)
    const navLinks = sidebar.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                closeSidebar();
            }
        });
    });
    
    // Cerrar sidebar al redimensionar ventana
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            closeSidebar();
        }
    });
    
    // Manejar tecla Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && sidebar.classList.contains('active')) {
            closeSidebar();
        }
    });
});