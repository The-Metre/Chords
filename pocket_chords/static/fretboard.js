const root = document.documentElement;

const fretboard = document.querySelector('.fretboard');
const number_of_frets = 24;
const number_of_strings = 6;

const single_fret_mark_positions = [3, 5, 7, 9, 15, 17, 19, 21];
const double_fret_mark_positions = [12, 24];

const flat_notes = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab'];
const sharp_notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#','G', 'G#'];

const guitar_tuning = [7, 2, 10, 5, 0, 7];

let accidentals = 'sharps';

// Const contain function, that initializes
// guitar fretboard with choosen numbers of strings and frets
const fretboard_app = {
    init() {
        this.setUpFretboard();
    },
    setUpFretboard() {
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
                
                let note_name = this.generate_notes_name((fret + guitar_tuning[i]), accidentals);
                fret_note.setAttribute('note-data', note_name);

                // If the fret of first string in single fretmark position
                // add a new class to it
                if (i === 0 && single_fret_mark_positions.indexOf(fret) !== -1) {
                    fret_note.classList.add('single-fretmark');
                }
                // same for double fretmark position
                if (i === 0 && double_fret_mark_positions.indexOf(fret) !== -1 ) {
                    fret_note.classList.add('double-fretmark');
                }
            }
        }
    },
    generate_notes_name(note_index, accidentals) {
        note_index = note_index % 12;
        let note_name;
        if (accidentals === 'flats') {
            note_name = flat_notes[note_index];
        } else if (accidentals ==='sharps') {
            note_name = sharp_notes[note_index];
        }
        return note_name;
    }
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