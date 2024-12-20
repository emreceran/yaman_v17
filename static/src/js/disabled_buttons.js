odoo.define('yaman.v17.disabled_buttons', function (require) {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {
        // Butonları seç
        const sarimButton = document.querySelector(".sarim-emri-btn");
        const catimButton = document.querySelector(".catim-emri-btn");
        const cncButton = document.querySelector(".cnc-emri-btn");
        const plastikButton = document.querySelector(".plastik-emri-btn");

        // Butonlara göre disabled durumlarını ayarla
        if (sarimButton && sarimButton.dataset.disabled === "true") {
            sarimButton.disabled = true;
        }
        if (catimButton && catimButton.dataset.disabled === "true") {
            catimButton.disabled = true;
        }
        if (cncButton && cncButton.dataset.disabled === "true") {
            cncButton.disabled = true;
        }
        if (plastikButton && plastikButton.dataset.disabled === "true") {
            plastikButton.disabled = true;
        }
    });
});
