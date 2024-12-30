document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    let bannerVisible = false;
    let bannerElement = null;
    let currentBannerId = null;

    // Função para verificar se devemos mostrar o banner
    function shouldShowBanner() {
        const lastShownTime = localStorage.getItem('lastBannerShownTime');
        if (!lastShownTime) return true;

        const now = new Date().getTime();
        const timeSinceLastShow = now - parseInt(lastShownTime);
        const fiveMinutesInMs = 5 * 60 * 1000; // 5 minutos em milissegundos

        return timeSinceLastShow >= fiveMinutesInMs;
    }

    // Função para registrar quando o banner foi mostrado
    function markBannerAsShown() {
        localStorage.setItem('lastBannerShownTime', new Date().getTime().toString());
    }

    // Função para buscar o próximo banner
    async function fetchNextBanner() {
        try {
            const response = await fetch('/banners/api/next-banner/');
            if (!response.ok) {
                console.error('Error fetching banner:', await response.text());
                return null;
            }
            const data = await response.json();
            console.log('Banner data:', data);
            return data;
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    }

    // Função para registrar click
    window.registerClick = async function(bannerId) {
        try {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            await fetch(`/banners/api/register-click/${bannerId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            });
        } catch (error) {
            console.error('Error registering click:', error);
        }
    }

    // Função para registrar visualização
    async function registerView(bannerId) {
        try {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            await fetch(`/banners/api/register-view/${bannerId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            });
        } catch (error) {
            console.error('Error registering view:', error);
        }
    }

    // Função para esconder o banner
    function hideBanner() {
        if (bannerElement && bannerElement.parentNode) {
            bannerElement.parentNode.removeChild(bannerElement);
            bannerElement = null;
            bannerVisible = false;
            currentBannerId = null;
        }
    }

    // Função para pré-carregar imagem
    function preloadImage(url) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => resolve(img);
            img.onerror = reject;
            img.src = url;
        });
    }

    // Função para criar o banner
    async function createBanner(banner) {
        console.log('Creating banner with image:', banner.imagem);
        
        if (currentBannerId === banner.id) {
            return null;
        }

        try {
            // Pré-carrega a imagem
            await preloadImage(banner.imagem);

            const div = document.createElement('div');
            div.id = 'floating-banner';
            div.className = 'floating-banner';
            
            div.innerHTML = `
                <div class="banner-content">
                    <button type="button" class="close-button">&times;</button>
                    <a href="${banner.link}" target="_blank" class="banner-inner" onclick="registerClick(${banner.id})">
                        <img src="${banner.imagem}" alt="Banner Publicitário" onerror="this.style.display='none'">
                    </a>
                </div>
            `;

            // Adiciona evento de clique no botão de fechar
            const closeButton = div.querySelector('.close-button');
            closeButton.onclick = function(e) {
                e.preventDefault();
                e.stopPropagation();
                hideBanner();
            };

            currentBannerId = banner.id;
            return div;
        } catch (error) {
            console.error('Error creating banner:', error);
            return null;
        }
    }

    // Função para mostrar o banner
    async function showBanner() {
        // Verifica se deve mostrar o banner baseado no tempo
        if (!shouldShowBanner()) {
            console.log('Aguardando tempo mínimo entre banners...');
            return;
        }

        if (bannerVisible) return;

        const banner = await fetchNextBanner();
        if (!banner) return;

        const bannerDiv = await createBanner(banner);
        if (!bannerDiv) return;

        document.body.appendChild(bannerDiv);
        bannerVisible = true;
        bannerElement = bannerDiv;
        
        // Registra a visualização do banner após ele ser exibido
        try {
            await registerView(banner.id);
            console.log('Banner view registered successfully');
        } catch (error) {
            console.error('Failed to register banner view:', error);
        }
        
        markBannerAsShown(); // Registra o momento em que o banner foi mostrado
    }

    // Função para rotacionar banners
    async function rotateBanners() {
        if (shouldShowBanner()) {
            hideBanner(); // Remove o banner atual
            await showBanner(); // Mostra o próximo banner
        }
    }

    // Mostrar primeiro banner apenas se necessário
    if (shouldShowBanner()) {
        setTimeout(showBanner, 3000);
    }

    // Tentar rotacionar banners a cada 5 minutos
    setInterval(rotateBanners, 300000); // 5 minutos em milissegundos
});
