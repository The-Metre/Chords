
const checkboxList = document.getElementById('checkbox-list');
const autocompleteInput = document.getElementById('autocomplete-input');
const stuff = JSON.parse(document.getElementById('chord_stuff').textContent)
const searching_chord_name = document.querySelector('.chord-name')
const searching_chord_tones =  document.querySelector('.chord-notes')


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


/* 
    Check if caseinsensitive key 
    contain in dictionary object('chord name': 'chord tones')
*/
function getParameterCaseInsensitive(object, key) {
    const asLowercase = key.toLowerCase();
    return object[Object.keys(object)
      .find(k => k.toLowerCase() === asLowercase)
    ];
  }
  
/* On click on the input area, show hints of chords names */
autocompleteInput.addEventListener('click', function() {
    checkboxList.style.display = 'block';
});

/* When Enter key pressed show chord tones */
autocompleteInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const checked_chord_name = autocompleteInput.value;
        const checked_chord_notes = getParameterCaseInsensitive(stuff, checked_chord_name);
        if (checked_chord_notes) {
            searching_chord_name.innerHTML = checked_chord_name;
            searching_chord_tones.innerHTML = checked_chord_notes;
        }
    }
})

document.addEventListener('click', function(e) {
    if (!autocompleteInput.contains(e.target) || e.target.value.length === 0) {
        checkboxList.style.display = 'none';
    }
});

