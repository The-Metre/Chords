let edit = id => {
    let element = document.getElementById(id).getElementsByClassName('edit-chunk')[0];
    element.hidden = true;
    let save = document.getElementById(id).getElementsByClassName('save-chunk')[0];
    save.hidden = false;
    let text = document.getElementById(id).getElementsByClassName('chunk-input')[0];
    text.hidden = false;
    let some = document.getElementById(id)
    some.display = 'none'
}

let save = id => {
    let element = document.getElementById(id).getElementsByClassName('edit-chunk')[0];
    element.hidden = false;
    let save = document.getElementById(id).getElementsByClassName('save-chunk')[0];
    save.hidden = true;


    fetch(`/edit/chunk/${id.split('data-')[1]}`)
    .then(response => response.json())
    .then(result => {
        console.log(result.text)})
}


const text = document.querySelector('.song_text')
const item = 'Em'
const chunk = new RegExp(item, "g")

function rep() {
    text.innerHTML
        = text.innerHTML
        .replace(chunk, `<span class='chord' value='${item}'>${item}</span>`)};