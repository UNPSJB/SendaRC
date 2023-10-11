$(document).ready(
  function () {
    $('.table').DataTable({
      "pageLength": 8,
    "lengthChange": false,
    });
    $("#id_localidad").autocomplete({
      source:'altaCliente/',
    });
  }
); //esto hay que mejorarlo

