document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
})


const chord_sign = document.querySelector('.song_text')
const item = 'Em'
const chunk = new RegExp(item, "g")

function rep() {
    chord_sign.innerHTML
        = chord_sign.innerHTML
        .replace(chunk, `<span class='chord' value='${item}'>${item} s</span>`)};