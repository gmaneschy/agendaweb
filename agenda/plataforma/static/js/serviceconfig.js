document.addEventListener("DOMContentLoaded", function () {
    const empresaForm = document.getElementById("service-form");
    const especialidadesFormMain = document.getElementById("especialidades-form-main");
    const continuarBtn = document.getElementById("continuar-btn");
    const addEspecialidadeBtn = document.getElementById("add-especialidade-btn");
    const listaEspecialidades = document.getElementById("lista-especialidades");
    const especialidadeForm = document.querySelector("#especialidade-form-container form") || especialidadesFormMain;
    const voltarBtn = document.querySelector(".btn-voltar");

    // Etapas
    const empresaStep = document.getElementById("empresa-form");
    const especialidadesStep = document.getElementById("especialidades-form");

    // 1. Enviar dados da empresa e ir para especialidades
    continuarBtn.addEventListener("click", function () {
        const formData = new FormData(empresaForm);
        formData.append("save_service", "1");

        fetch("", {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCSRFToken(),
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                empresaStep.classList.remove("active");
                especialidadesStep.classList.add("active");
            } else {
                alert("Erro ao salvar dados da empresa.");
                console.error(data.errors);
            }
        });
    });

    // 2. Adicionar nova especialidade via AJAX
    addEspecialidadeBtn.addEventListener("click", function () {
        const formData = new FormData(especialidadeForm);
        formData.append("add_especialidade", "1");

        fetch("", {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCSRFToken(),
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const div = document.createElement("div");
                div.classList.add("especialidade-item");
                div.innerHTML = `
                    <p>
                      <strong>${data.nome}</strong> - R$ ${data.preco}
                      <a href="#" data-id="${data.id}" class="remover-especialidade">[Remover]</a>
                    </p>
                `;
                listaEspecialidades.appendChild(div);
                especialidadeForm.reset();
            } else {
                alert("Erro ao adicionar serviço.");
                console.error(data.errors);
            }
        });
    });

    // 3. Remover especialidade via AJAX - updated version
    document.addEventListener("click", function (e) {
    if (e.target.classList.contains("remover-especialidade")) {
        e.preventDefault();
        const id = e.target.dataset.id;

        fetch(`/remover_especialidade/${id}/`, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCSRFToken()
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const item = e.target.closest(".especialidade-item");
                item.remove();

                // Show "no services" message if list is empty
                if (listaEspecialidades.querySelectorAll('.especialidade-item').length === 0) {
                    listaEspecialidades.innerHTML = '<p>Nenhum serviço cadastrado ainda.</p>';
                }
            } else {
                alert("Erro ao remover especialidade: " + (data.error || ''));
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Erro na comunicação com o servidor. Detalhes no console.");
        });
    }
});

    // 4. Voltar ao formulário da empresa
    voltarBtn.addEventListener("click", function () {
        especialidadesStep.classList.remove("active");
        empresaStep.classList.add("active");
    });

    // Função para obter CSRF
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});

document.querySelector(".btn-finalizar").addEventListener("click", function (e) {
    especialidadesFormMain.submit();
});
