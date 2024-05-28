function initializeDataTable() {
  $(".datatableEntity").DataTable({
    pageLength: 10,
    lengthChange: false,
    columnDefs: [{ orderable: false, targets: -1 }],
    language: {
      info: "Mostrando _END_ de _TOTAL_ registros",
      paginate: {
        previous: "Anterior",
        next: "Siguiente",
      },
    },
    order: [[0, "desc"]],
  });
}

document.addEventListener("DOMContentLoaded", function () {
  const btnLightMode = document.getElementById("btn-LightMode");
  const btnDarkMode = document.getElementById("btn-DarkMode");
  const navContainer = document.querySelector(".nav-container");
  const sideBar = document.querySelector(".navbar");
  const expandButton = document.getElementById("expand-button");
  const logo = document.getElementById('logo')
  const mainContainer = document.querySelector(".container-seccion-main");
  const isExpanded = localStorage.getItem("isNavExpanded") === "true";
  const currentTheme = localStorage.getItem("theme") || "dark";

  navContainer.classList.add("no-transition");
  mainContainer.classList.add("no-transition");

  initializeDataTable();

  if (isExpanded) {
    expandSidebar();
  }

  if (currentTheme === "light") {
    enableLightMode();
    toggleIcon("light");
  }

  setTimeout(() => {
    navContainer.classList.remove("no-transition");
    mainContainer.classList.remove("no-transition");
  }, 200);

  expandButton.addEventListener("click", function () {
    navContainer.classList.toggle("expanded");
    sideBar.classList.toggle("sideBarExpand");
    mainContainer.classList.toggle("mainExpanded");
    
    localStorage.setItem(
      "isNavExpanded",
      navContainer.classList.contains("expanded")
    );
  });

  btnLightMode.addEventListener("click", function () {
    toggleTheme("light");
    toggleIcon("light");
  });

  btnDarkMode.addEventListener("click", function () {
    toggleTheme("dark");
    toggleIcon("dark");
  });

  function toggleTheme(mode) {
    if (mode === "light") {
      enableLightMode();
    } else if (mode === "dark") {
      disableLightMode();
    }
  }

  function toggleIcon(theme) {
    const iconElement = document.getElementById("bd-theme").querySelector("i");

    if (theme === "light") {
      iconElement.classList.remove("bi-moon-stars");
      iconElement.classList.add("bi-brightness-high");
    } else if (theme === "dark") {
      iconElement.classList.remove("bi-brightness-high");
      iconElement.classList.add("bi-moon-stars");
    }
  }

  function enableLightMode() {
    const body = document.body;
    btnDarkMode.classList.remove("active");
    btnLightMode.classList.add("active");
    body.classList.add("light-mode");
    document
      .querySelectorAll(".other-light-elements")
      .forEach(function (element) {
        element.classList.add("light-mode");
      });
    localStorage.setItem("theme", "light");
  }

  function disableLightMode() {
    const body = document.body;
    btnLightMode.classList.remove("active");
    btnDarkMode.classList.add("active");
    body.classList.remove("light-mode");
    document
      .querySelectorAll(".other-light-elements")
      .forEach(function (element) {
        element.classList.remove("light-mode");
      });
    localStorage.setItem("theme", "dark");
  }

  function expandSidebar() {
    navContainer.classList.add("expanded");
    sideBar.classList.add("sideBarExpand");
    mainContainer.classList.add("mainExpanded");
  }
});

$(function () {
  $("#offcanvasExample").on("show.bs.offcanvas", function (event) {
    var button = $(event.relatedTarget);
    var url = button.data("url");
    var modal = $(this);
    modal.find(".offcanvas-body").load(url);
  });
});
