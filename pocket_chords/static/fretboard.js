const root = document.documentElement;

const fretboard = document.querySelector('.fretboard');
const selected_instrument_selector = document.querySelector('#instrument-selector'); 
const accidentals_selector = document.querySelector('.accidental-selector'); 
const number_of_frets_selector = document.querySelector('#number-of-frets');

const single_fret_mark_positions = [3, 5, 7, 9, 15, 17, 19, 21];
const double_fret_mark_positions = [12, 24];

const flat_notes = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab'];
const sharp_notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#','G', 'G#'];

const instrument_tuning_presets = {
    "Guitar": [7, 2, 10, 5, 0, 7],
    "Bass (4 strings)": [10, 5, 0, 7],
    'Ukulele': [0, 7, 3, 10],
};

let selected_instrument = 'Guitar';
let number_of_frets = 12;
let number_of_strings = instrument_tuning_presets[selected_instrument].length;
let accidentals = 'sharps';


// Const contain function, that initializes
// guitar fretboard with choosen numbers of strings and frets
const fretboard_app = {
    init() {
        this.setup_fretboard();
        this.setup_selected_instrument();
        this.setup_event_listeners();
    },
    setup_fretboard() {
        fretboard.innerHTML = '';
        root.style.setProperty('--number-of-strings', number_of_strings);
        // Add strings to fretboard
        for (let i = 0; i < number_of_strings; i++) {
            let string = fretboard_tools.createElement('div');
            string.classList.add('string');
            fretboard.appendChild(string)

            // Add frets to the string
            for (let fret = 0; fret <= number_of_frets; fret++) {
                let fret_note = fretboard_tools.createElement('div');
                fret_note.classList.add('fret-note');
                string.appendChild(fret_note);
                
                let note_name = this.generate_notes_name((fret + instrument_tuning_presets[selected_instrument][i]), accidentals);
                fret_note.setAttribute('note-data', note_name);

                // If the fret of first string in single fretmark position
                // add a new class to it
                if (i === 0 && single_fret_mark_positions.indexOf(fret) !== -1) {
                    fret_note.classList.add('single-fretmark');
                }
                // same for double fretmark position
                if (i === 0 && double_fret_mark_positions.indexOf(fret) !== -1) {
                    let double_fretmark = fretboard_tools.createElement('div');
                    double_fretmark.classList.add('double-fretmark');
                    fret_note.appendChild(double_fretmark);
                }
            }
        }
    },
    // Return a note, based on list of notes,
    // that passed in the function (flats or sharps)
    generate_notes_name(note_index, accidentals) {
        note_index = note_index % 12;
        let note_name;
        if (accidentals === 'flats') {
            note_name = flat_notes[note_index];
        } else if (accidentals ==='sharps') {
            note_name = sharp_notes[note_index];
        }
        return note_name;
    },
    // Fill instrement selector with options
    setup_selected_instrument() {
        for (instrument in instrument_tuning_presets) {
            let instrument_option = fretboard_tools.createElement('option', instrument);
            selected_instrument_selector.appendChild(instrument_option);
        }
    },
    
    setup_event_listeners() {
        // Add listeners to each fret, when hover on it by the mouse
        // change opacity, so a note of the fret will be visible
        fretboard.addEventListener('mouseover', (event) => {
            if (event.target.classList.contains('fret-note')) {
                event.target.style.setProperty('--note-dot-opacity', 1);
            }

        });
        // When mouse out from the fret, change it opactity
        // to zero
        fretboard.addEventListener('mouseout', (event) => {
            event.target.style.setProperty('--note-dot-opacity', 0);
        });
        // Whe user switch instrument options,
        // change number of strings value, based on an instrument
        selected_instrument_selector.addEventListener('change', (event) => {
            selected_instrument = event.target.value;
            number_of_strings = instrument_tuning_presets[selected_instrument].length;
            this.setup_fretboard();
        });
        // Whe user switch accidental options,
        // change a type of notes notation (flats or sharps)
        accidentals_selector.addEventListener('click', (event) => {
            if (event.target.classList.contains('acc-select')) {
                accidentals = event.target.value;
                this.setup_fretboard();
            } else {
                return;
            }
        });
        // Add listener to input number,
        // that change number of rendered frets of an instrument
        number_of_frets_selector.addEventListener('change', (event) => {
            number_of_frets = number_of_frets_selector.value;
            this.setup_fretboard();
        });
    },
}

// Const contain handy function to create html elements, and if needed
// with innerHTML content
const fretboard_tools = {
    createElement(element, content) {
        element = document.createElement(element);
        if (arguments.length > 1) {
            element.innerHTML = content;
        }
        return element;
    }
}


fretboard_app.init();