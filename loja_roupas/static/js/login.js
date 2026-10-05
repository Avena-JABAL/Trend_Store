document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll("[data-form-target]");
    const panels = document.querySelectorAll("[data-form-panel]");

    // O clique alterna a exibição; só o botão de envio faz uma requisição.
    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            const target = button.dataset.formTarget;

            panels.forEach(function (panel) {
                panel.hidden = panel.id !== target;
            });

            buttons.forEach(function (item) {
                item.setAttribute("aria-pressed", item === button ? "true" : "false");
            });
        });
    });
});