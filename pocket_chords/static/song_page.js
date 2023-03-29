let edit = id => {
    let element = document.getElementById(id).getElementsByClassName('edit-chunk')[0];
    element.hidden = true;
    let save = document.getElementById(id).getElementsByClassName('save-chunk')[0];
    save.hidden = false
}

let save = id => {
    let element = document.getElementById(id).getElementsByClassName('edit-chunk')[0];
    element.hidden = false;
    let save = document.getElementById(id).getElementsByClassName('save-chunk')[0];
    save.hidden = true;
    console.log('saving', id)
}