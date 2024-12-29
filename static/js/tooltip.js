document.addEventListener('DOMContentLoaded', function() {
    // Função para inicializar tooltips em elementos específicos
    function initializeTooltips() {
        const tooltipWords = document.querySelectorAll('.tooltip-word');
        
        tooltipWords.forEach(word => {
            // Garante que o tooltip seja posicionado corretamente
            word.addEventListener('mouseenter', function(e) {
                const tooltip = this.querySelector('.tooltip');
                if (tooltip) {
                    const rect = this.getBoundingClientRect();
                    const tooltipRect = tooltip.getBoundingClientRect();
                    
                    // Ajusta posição horizontal se necessário
                    if (rect.left + tooltipRect.width > window.innerWidth) {
                        tooltip.style.left = 'auto';
                        tooltip.style.right = '0';
                    }
                    
                    // Ajusta posição vertical se necessário
                    if (rect.top - tooltipRect.height < 0) {
                        tooltip.style.bottom = 'auto';
                        tooltip.style.top = '100%';
                    }
                }
            });
        });
    }

    // Inicializa tooltips na carga da página
    initializeTooltips();

    // Observa mudanças no DOM para reinicializar tooltips em conteúdo dinâmico
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                initializeTooltips();
            }
        });
    });

    // Configura o observer
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});