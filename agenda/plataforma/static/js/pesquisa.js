document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');

    function realizarPesquisa() {
        const termo = searchInput.value.toLowerCase();

        document.querySelectorAll('#tabela-servicos tbody tr').forEach(row => {
            const nomeServico = row.cells[0].textContent.toLowerCase();

            if (nomeServico.includes(termo)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    searchInput.addEventListener('input', realizarPesquisa);

    document.getElementById('clear-filters').addEventListener('click', () => {
        searchInput.value = '';
        realizarPesquisa();
    });
});