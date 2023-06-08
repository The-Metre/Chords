const checkboxList = document.getElementById('checkbox-list');
const autocompleteInput = document.getElementById('autocomplete-input');
const stuff = JSON.parse(document.getElementById('chord_stuff').textContent)


const options = [];
for (const [item,_] of Object.entries(stuff)) {
    options.push(item)
};


function createCheckbox(option){
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.value = option;
    checkbox.id = option;
    const label = document.createElement('label');
    label.htmlFor = option;
    label.appendChild(document.createTextNode(option));
    checkboxList.appendChild(checkbox);
    checkboxList.appendChild(label);
};

options.forEach(createCheckbox);

autocompleteInput.addEventListener('input', function() {
    const inputValue = this.value.toLowerCase();
    const checkboxes = checkboxList.getElementsByTagName('input');
    for (let i = 0; i < checkboxes.length; i++) {
        const label = checkboxes[i].nextSibling;
        if (label.innerHTML.toLowerCase().indexOf(inputValue) > -1) {
            checkboxes[i].style.display = '';
            label.style.display = '';
        } else {
            checkboxes[i].style.display = 'none';
            label.style.display = 'none';
        }
    }
});

autocompleteInput.addEventListener('click', function() {
    checkboxList.style.display = 'block';
});

document.addEventListener('click', function(e) {
    if (!autocompleteInput.contains(e.target)) {
        checkboxList.style.display = 'none';
    }
});
