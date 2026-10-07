document.addEventListener("DOMContentLoaded", function () {
  const totalItens = document.getElementById("total-itens");
  const totalPagar = document.getElementById("total-pagar");
  const selecionarTodos = document.getElementById("selecionar-todos");
  const excluirSelecionados = document.getElementById("excluir-selecionados");

  function converterPreco(valor) {
    let texto = String(valor).trim();

    texto = texto.replace("R$", "").trim();

    if (texto.includes(",")) {
      texto = texto.replace(/\./g, "");
      texto = texto.replace(",", ".");
    }

    const numero = Number(texto);

    return Number.isFinite(numero) ? numero : 0;
  }

  function atualizarCarrinho() {
    const checkboxes = document.querySelectorAll(".item-checkbox-input");

    let quantidade = 0;
    let total = 0;

    checkboxes.forEach(function (checkbox) {
      const card = checkbox.closest(".item-card");

      if (checkbox.checked) {
        quantidade++;

        const preco = converterPreco(card.dataset.preco);
        const quantidadeItem = Number(card.dataset.quantidade) || 0;

        total += preco * quantidadeItem;

        card.classList.add("selecionado");
      } else {
        card.classList.remove("selecionado");
      }
    });

    totalItens.textContent = quantidade;

    totalPagar.textContent = total.toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });

    excluirSelecionados.disabled = quantidade === 0;

    selecionarTodos.checked =
      checkboxes.length > 0 && quantidade === checkboxes.length;
  }

  document.addEventListener("change", function (event) {
    if (event.target.classList.contains("item-checkbox-input")) {
      atualizarCarrinho();
    }
  });

  selecionarTodos.addEventListener("change", function () {
    const checkboxes = document.querySelectorAll(".item-checkbox-input");

    checkboxes.forEach(function (checkbox) {
      checkbox.checked = selecionarTodos.checked;
    });

    atualizarCarrinho();
  });

  excluirSelecionados.addEventListener("click", function () {
    const selecionados = document.querySelectorAll(
      ".item-checkbox-input:checked",
    );

    if (selecionados.length === 0) {
      return;
    }

    const confirmar = confirm(
      `Deseja excluir ${selecionados.length} item(ns) selecionado(s)?`,
    );

    if (!confirmar) {
      return;
    }

    const form = document.createElement("form");

    form.method = "POST";
    form.action = "/carrinho/remover-selecionados/";

    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]",
    ).value;

    const csrfInput = document.createElement("input");
    csrfInput.type = "hidden";
    csrfInput.name = "csrfmiddlewaretoken";
    csrfInput.value = csrfToken;

    form.appendChild(csrfInput);

    selecionados.forEach(function (checkbox) {
      const card = checkbox.closest(".item-card");
      const produtoId = card.dataset.produtoId;

      const input = document.createElement("input");

      input.type = "hidden";
      input.name = "produtos";
      input.value = produtoId;

      form.appendChild(input);
    });

    document.body.appendChild(form);
    form.submit();
  });

  atualizarCarrinho();
});
