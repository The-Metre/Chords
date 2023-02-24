const root = document.documentElement;

const fretboard = document.querySelector('.fretboard');
const selected_instrument_selector = document.querySelector('#instrument-selector'); 
const accidentals_selector = document.querySelector('.accidental-selector'); 
const number_of_frets_selector = document.querySelector('#number-of-frets');
const show_all_notes_selector = document.querySelector('#show-all-notes');
const show_duplicate_notes_selector = document.querySelector('#show-duplicate-notes');
const note_name_section = document.querySelector('.note-name-section');

const single_fret_mark_positions = [3, 5, 7, 9, 15, 17, 19, 21];
const double_fret_mark_positions = [12, 24];

const flat_notes = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab'];
const sharp_notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#','G', 'G#'];

const instrument_tuning_presets = {
    "Guitar": [7, 2, 10, 5, 0, 7],
    "Bass (4 strings)": [10, 5, 0, 7],
    'Ukulele': [0, 7, 3, 10],
};

let all_notes;
let show_duplicate_notes = false;

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
        this.setup_note_name_section();
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
    /*  */
    setup_note_name_section() {
        note_name_section.innerHTML = '';
        let note_names;
        if (accidentals === 'flats') {
            note_names = flat_notes;
        } else {
            note_names = sharp_notes;
        }
        note_names.forEach((note_name) => {
            let note_name_element = fretboard_tools.createElement('span', note_name);
            note_name_section.appendChild(note_name_element);
        });
    },
    /*  */
    show_note_dot(event) {
        if (event.target.classList.contains('fret-note')) {
            if (show_duplicate_notes) {
                fretboard_app.toggle_duplicate_notes(event.target.getAttribute('note-data'), 1);
            } else {
                event.target.style.setProperty('--note-dot-opacity', 1);
            }
        }
    },
    /*  */
    hide_note_dot(event) {
        if (show_duplicate_notes) {
            fretboard_app.toggle_duplicate_notes(event.target.getAttribute('note-data'), 0);
        } else {
            event.target.style.setProperty('--note-dot-opacity', 0);
        }
    },

    setup_event_listeners() {
        // Add listeners to each fret, when hover on it by the mouse
        // change opacity, so a note of the fret will be visible
        fretboard.addEventListener('mouseover', this.show_note_dot);
        // When mouse out from the fret, change it opactity
        // to zero
        fretboard.addEventListener('mouseout', this.hide_note_dot);

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
                this.setup_note_name_section();
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
        //
        show_all_notes_selector.addEventListener('change', () => {
            // Remove event listeners from notes, when
            // show-all-notes flag are checked
            if (show_all_notes_selector.checked) {
                root.style.setProperty('--note-dot-opacity', 1);

                fretboard.removeEventListener('mouseover', this.show_note_dot);
                fretboard.removeEventListener('mouseout', this.hide_note_dot);
                this.setup_fretboard();
                // Add the event listeners if flag removed
            } else {
                root.style.setProperty('--note-dot-opacity', 0);

                fretboard.addEventListener('mouseover', this.show_note_dot);
                fretboard.addEventListener('mouseout', this.hide_note_dot);
                this.setup_fretboard();
            }
        });
        /* Realization of a toggle event on the checkbox */
        show_duplicate_notes_selector.addEventListener('change', () => {
            show_duplicate_notes = !show_duplicate_notes;
        });
        /*  */
        note_name_section.addEventListener('mouseover', (event) => {
             let note_to_show = event.target.innerText;
             fretboard_app.toggle_duplicate_notes(note_to_show, 1);
        });
        /*  */
        note_name_section.addEventListener('mouseout', (event) => {
            if (!show_all_notes_selector.checked) {
                let note_to_show = event.target.innerText;
                fretboard_app.toggle_duplicate_notes(note_to_show, 0);
            } else {
                return;
            }
        });
    },

    /* When checkbox flag toggled
        change opacity of a target note
    */
    toggle_duplicate_notes(note_name, opacity) {
        all_notes = document.querySelectorAll('.fret-note');
        for (let i = 0; i < all_notes.length; i++) {
            if (all_notes[i].getAttribute('note-data') === note_name) {
                all_notes[i].style.setProperty('--note-dot-opacity', opacity); 
            }
        }
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