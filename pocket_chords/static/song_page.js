document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
})


const text = document.querySelector('.song_text')
const item = 'Em'
const chunk = new RegExp(item, "g")

function rep() {
    text.innerHTML
        = text.innerHTML
        .replace(chunk, `<span class='chord' value='${item}'>${item}</span>`)};