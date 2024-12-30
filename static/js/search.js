// Namespace para o aplicativo de busca
const SearchApp = {
    init: function() {
        const searchInput = document.getElementById('searchInput');
        const searchResults = document.getElementById('searchResults');
        const searchClear = document.getElementById('searchClear');
        let resultsList;
        let searchTimeout;

        // Garantir que temos a lista de resultados
        if (!searchResults.querySelector('.list-group')) {
            resultsList = document.createElement('div');
            resultsList.className = 'list-group';
            searchResults.appendChild(resultsList);
        } else {
            resultsList = searchResults.querySelector('.list-group');
        }

        // Função para realizar a busca
        function performSearch(query) {
            if (!query) {
                searchResults.style.display = 'none';
                return;
            }

            // Mostrar indicador de carregamento
            resultsList.innerHTML = '<div class="list-group-item">Buscando...</div>';
            searchResults.style.display = 'block';

            fetch(`/search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    resultsList.innerHTML = '';
                    
                    if (data.results && data.results.length > 0) {
                        data.results.forEach(result => {
                            const item = document.createElement('a');
                            item.href = result.url;
                            item.className = 'list-group-item list-group-item-action';
                            item.innerHTML = `
                                <div class="d-flex justify-content-between">
                                    <h6 class="mb-1">${result.title}</h6>
                                </div>
                                <p class="mb-1">${result.text}</p>
                            `;
                            resultsList.appendChild(item);
                        });
                        searchResults.style.display = 'block';
                    } else {
                        resultsList.innerHTML = '<div class="list-group-item">Nenhum resultado encontrado</div>';
                        searchResults.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('Erro na busca:', error);
                    resultsList.innerHTML = '<div class="list-group-item text-danger">Erro ao realizar a busca</div>';
                    searchResults.style.display = 'block';
                });
        }

        // Event listener para input de busca com debounce
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                const query = this.value.trim();
                
                if (query) {
                    searchTimeout = setTimeout(() => performSearch(query), 300);
                } else {
                    searchResults.style.display = 'none';
                }
            });
        }

        // Event listener para botão limpar
        if (searchClear) {
            searchClear.addEventListener('click', function() {
                searchInput.value = '';
                searchResults.style.display = 'none';
            });
        }

        // Fechar resultados ao clicar fora
        document.addEventListener('click', function(e) {
            if (searchResults && !searchResults.contains(e.target) && e.target !== searchInput) {
                searchResults.style.display = 'none';
            }
        });
    }
};

// Inicializar o aplicativo quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    SearchApp.init();
});
