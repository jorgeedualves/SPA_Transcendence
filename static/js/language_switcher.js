// static/js/language_switcher.js

function switchLanguage(language) {
    fetch("/core/switch_language/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie('csrftoken')  // Função para pegar o token CSRF
        },
        body: `language=${language}`
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                fetchTranslatedTexts();  // Busca o conteúdo traduzido
            } else {
                console.error('Error switching language');
            }
        })
        .catch(error => console.error('Error:', error));
}

function fetchTranslatedTexts() {
    fetch("/core/get_translated_texts/")
        .then(response => response.json())
        .then(data => {
            document.querySelector('.navList a[href="/game/options"]').innerText = data.language;
            document.querySelector('.navList a[href="/game/options"]').innerText = data.play;
            document.querySelector('.navList a[href="/account"]').innerText = data.profile;
            document.querySelector('button.btn-secondary').innerText = data.add;
            document.querySelector('.customHistory h2').innerText = data.match_history;
            document.querySelector('.customHistory a').innerText = data.view_more;
            document.querySelector('.customStatistics h2').innerText = data.statistics;
            document.querySelector('.customStatistics a').innerText = data.view_more;
            document.querySelector('footer').innerText = data.made_by_pong;
        })
        .catch(error => console.error('Error fetching translations:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
