function initializeDataTable() {
  const table = document.querySelector('.table');
  if (table) {
    const dataTable = new DataTable(table, {
      pageLength: 8,
      lengthChange: false,
    });
  }
}
document.addEventListener("DOMContentLoaded", function () {
  initializeDataTable();
  const navContainer = document.querySelector(".nav-container");
  const sideBar = document.querySelector(".navbar");
  const expandButton = document.getElementById("expand-button");

  // Desactivar la transición al cargar la página
  navContainer.classList.add("no-transition");

  const isExpanded = localStorage.getItem("isNavExpanded") === "true";

  if (isExpanded) {
    navContainer.classList.add("expanded");
    sideBar.classList.add("sideBarExpand");
  }

  // Habilitar la transición después de un pequeño retraso
  setTimeout(() => {
    navContainer.classList.remove("no-transition");
  }, 100);

  expandButton.addEventListener("click", function () {
    navContainer.classList.toggle("expanded");
    sideBar.classList.toggle("sideBarExpand");
    localStorage.setItem("isNavExpanded", navContainer.classList.contains("expanded"));
  });
});

$(function() {
    $('#offcanvasExample').on('show.bs.offcanvas', function (event) {
var button = $(event.relatedTarget) // Button that triggered the modal
var url = button.data('url') // Extract info from data-* attributes
// If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
// Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
var modal = $(this)
modal.find('.offcanvas-body').load(url);
})

})