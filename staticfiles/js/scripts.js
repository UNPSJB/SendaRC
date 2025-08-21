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
