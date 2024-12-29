// Debug utilities
const debugLogger = {
    init() {
        console.log('Debug initialized');
        this.checkFontLoading();
        this.checkAPIEndpoints();
        this.checkAudioElements();
    },

    checkFontLoading() {
        document.fonts.ready.then(() => {
            const fontLoaded = document.fonts.check('1em "Estrangelo Edessa"');
            console.log('Estrangelo Edessa font loaded:', fontLoaded);
        });
    },

    checkAPIEndpoints() {
        const bookSelect = document.getElementById('book-select');
        if (bookSelect) {
            console.log('Book select found:', bookSelect.value);
            bookSelect.addEventListener('change', (e) => {
                console.log('Book selection changed:', e.target.value);
                console.log('Attempting to fetch chapters from:', `/get-chapters/?book_id=${e.target.value}`);
            });
        } else {
            console.error('Book select element not found');
        }
    },
    checkAudioElements() {
        const audioElements = document.querySelectorAll('audio');
        audioElements.forEach(audio => {
            const src = audio.querySelector('source').getAttribute('src');
            console.log('Audio element found with source:', src);
            audio.addEventListener('error', (e) => {
                console.error('Error loading audio:', src, e);
            });
            audio.addEventListener('loadeddata', () => {
                console.log('Audio loaded successfully:', src);
            });
        });
    }
};

// Initialize debug logging
document.addEventListener('DOMContentLoaded', () => {
    debugLogger.init();
});
