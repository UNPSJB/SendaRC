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

