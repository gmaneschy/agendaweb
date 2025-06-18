document.addEventListener("DOMContentLoaded", function () {
  const cepInput = document.getElementById("id_cep");
  const erroCepInvalido = document.getElementById("erro-cep-invalido");
  const erroCepDigitos = document.getElementById("erro-cep-digitos");

  cepInput.addEventListener("blur", async function () {
    const cep = cepInput.value.replace(/\D/g, "");

    // Esconde todos os avisos antes de fazer qualquer verificação
    erroCepInvalido.style.display = "none";
    erroCepDigitos.style.display = "none";

    if (cep.length !== 8) {
      erroCepDigitos.style.display = "block";
      return;
    }

    try {
      const response = await fetch(`https://brasilapi.com.br/api/cep/v1/${cep}`);
      if (!response.ok) {
        erroCepInvalido.style.display = "block";
        return;
      }

      const data = await response.json();

      document.getElementById("id_rua").value = data.street || "";
      document.getElementById("id_bairro").value = data.neighborhood || "";
      document.getElementById("id_cidade").value = data.city || "";
      document.getElementById("id_estado").value = data.state || "";
    } catch (error) {
      erroCepInvalido.style.display = "block";
      console.error("Erro ao buscar CEP:", error);
    }
  });
});
