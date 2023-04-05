const edit = id => {
    let element = document.getElementById(id).getElementsByClassName('edit-chunk')[0];
    element.hidden = true;
    let save = document.getElementById(id).getElementsByClassName('save-chunk')[0];
    save.hidden = false;
    let text = document.getElementById(id).getElementsByClassName('chunk-input')[0];
    text.hidden = false;
    let some = document.getElementById(id)
    some.display = 'none'
}

const save = id => {
    const element = document.getElementById(id).getElementsByClassName('edit-chunk')[0];
    element.hidden = false;
    const save = document.getElementById(id).getElementsByClassName('save-chunk')[0];
    save.hidden = true;
    let text = document.getElementById(id).getElementsByClassName('chunk-input')[0];
    text.hidden = true;

    save.type = 'hidden'
    save.name = '_csrf'

    fetch(`/edit/chunk/${id.split('data-')[1]}`, {
        method: "PUT",
        body: JSON.stringify({
            song_chunk: text.value
        })
    })
    .then(response => response.json())
    .then(result => {
        one = document.getElementById(id).getElementsByClassName('chunk-text')[0];
        one.innerHTML = result.text
        }
        )
}


const text = document.querySelector('.song_text')
const item = 'Em'
const chunk = new RegExp(item, "g")

function rep() {
    text.innerHTML
        = text.innerHTML
        .replace(chunk, `<span class='chord' value='${item}'>${item}</span>`)};