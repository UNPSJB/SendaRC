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
});

document.addEventListener("DOMContentLoaded", function () {
  const navContainer = document.querySelector(".nav-container");
  const sideBar = document.querySelector(".navbar");
  const expandButton = document.getElementById("expand-button");

  const isExpanded = localStorage.getItem("isNavExpanded") === "true";

  if (isExpanded) {
    navContainer.classList.add("expanded");
    sideBar.classList.add("sideBarExpand");
  }

  expandButton.addEventListener("click", function () {
    navContainer.classList.toggle("expanded");
    sideBar.classList.toggle("sideBarExpand");
    localStorage.setItem("isNavExpanded", navContainer.classList.contains("expanded"));
  });
});
