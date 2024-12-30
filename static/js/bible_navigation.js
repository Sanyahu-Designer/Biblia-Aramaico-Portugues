document.addEventListener('DOMContentLoaded', function() {
    const bookSelect = document.getElementById('book-select');
    const chapterSelect = document.getElementById('chapter-select');
    
    async function loadChapters(bookId) {
        if (!bookId) {
            chapterSelect.innerHTML = '<option value="">Selecione um Capítulo</option>';
            chapterSelect.disabled = true;
            return;
        }

        try {
            const response = await fetch(`/get-chapters/?book_id=${bookId}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const chapters = await response.json();
            
            chapterSelect.innerHTML = '<option value="">Selecione um Capítulo</option>';
            chapters.forEach(chapter => {
                const option = document.createElement('option');
                option.value = chapter.id;  // Usar ID para navegação
                option.textContent = `Capítulo ${chapter.number}`;  // Mostrar apenas o número
                if (chapter.id === parseInt(selectedChapterId)) {
                    option.selected = true;
                }
                chapterSelect.appendChild(option);
            });
            chapterSelect.disabled = false;
        } catch (error) {
            console.error('Erro ao carregar capítulos:', error);
            chapterSelect.innerHTML = '<option value="">Erro ao carregar capítulos</option>';
            chapterSelect.disabled = true;
        }
    }

    // Carregar capítulos iniciais se um livro estiver selecionado
    if (bookSelect.value) {
        loadChapters(bookSelect.value);
    }

    // Event listeners
    bookSelect.addEventListener('change', function() {
        loadChapters(this.value);
    });

    chapterSelect.addEventListener('change', function() {
        if (this.value) {
            window.location.href = `/?book=${bookSelect.value}&chapter=${this.value}`;
        }
    });
});
