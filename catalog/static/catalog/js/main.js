"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const menuButton = document.querySelector(".menu-button");
    const mainNavigation = document.querySelector(".main-nav");

    if (!menuButton || !mainNavigation) {
        return;
    }

    function closeMenu() {
        mainNavigation.classList.remove("is-open");
        menuButton.setAttribute("aria-expanded", "false");
        menuButton.setAttribute("aria-label", "باز کردن منو");
    }

    function openMenu() {
        mainNavigation.classList.add("is-open");
        menuButton.setAttribute("aria-expanded", "true");
        menuButton.setAttribute("aria-label", "بستن منو");
    }

    menuButton.addEventListener("click", () => {
        const isOpen = mainNavigation.classList.contains("is-open");

        if (isOpen) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    mainNavigation.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", closeMenu);
    });

    document.addEventListener("click", (event) => {
        const clickedInsideMenu = mainNavigation.contains(event.target);
        const clickedButton = menuButton.contains(event.target);

        if (!clickedInsideMenu && !clickedButton) {
            closeMenu();
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeMenu();
        }
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth > 768) {
            closeMenu();
        }
    });
});