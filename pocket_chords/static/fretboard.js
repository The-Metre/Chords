(function() {
    const root = document.documentElement;
    const fretboard = document.querySelector('.fretboard');
    const instrument_selector = document.querySelector('#instrument-selector'); 
    const accidentals_selector = document.querySelector('.accidental-selector'); 
    const number_of_frets_selector = document.querySelector('#number-of-frets');
    const show_all_notes_selector = document.querySelector('#show-all-notes');
    const show_duplicate_notes_selector = document.querySelector('#show-duplicate-notes');
    const note_name_section = document.querySelector('.note-name-section');
    const show_guitar_fretboard_selector = document.querySelector('#show-guitar-fretboard');
    const show_metronome_selector = document.querySelector('#show-metronome');
    const show_interval_listener_selector = document.querySelector('#show-interval-listener');
    const metronome_container = document.querySelector('.metronome-container');
    const interval_container = document.querySelector('.intervals-container');
    const guitar_fretboard_container = document.querySelector('.fretboard-settings')
    const chord_name_section = document.querySelector('.chord-name-section')

    const chord_section = document.querySelectorAll('.chord-notes')

    const single_fret_mark_positions = [3, 5, 7, 9, 15, 17, 19, 21];
    const double_fret_mark_positions = [12, 24];
    const flat_notes = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab'];
    const sharp_notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#','G', 'G#'];
    const instrument_tuning_presets = {
        "Guitar": [7, 2, 10, 5, 0, 7],
        "Bass (4 strings)": [10, 5, 0, 7],
        'Ukulele': [0, 7, 3, 10],
    };

    const test = document.querySelector('.test')

    let all_notes;
    let show_duplicate_notes = false;
    let show_all_notes = false;
    let selected_instrument = 'Guitar';
    let accidentals = 'sharps';
    let number_of_frets = 12;
    let number_of_strings = instrument_tuning_presets[selected_instrument].length;


    // Const contain function, that initializes
    // guitar fretboard with choosen numbers of strings and frets
    const fretboard_app = {
        init() {
            this.setup_fretboard();
            this.setup_selected_instrument();
            this.setup_note_name_section();
            fretboard_handlers.set_show_interval_listener();
            fretboard_handlers.set_show_metronome();
            fretboard_handlers.setup_event_listeners();
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
                instrument_selector.appendChild(instrument_option);
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

        toggle_duplicate_notes(note_name, opacity) {
        /* When checkbox flag toggled
            change opacity of a target note
        */
            all_notes = document.querySelectorAll('.fret-note');
            for (let i = 0; i < all_notes.length; i++) {
                if (all_notes[i].getAttribute('note-data') === note_name) {
                    all_notes[i].style.setProperty('--note-dot-opacity', opacity); 
                }
            }
        },
    }

    const fretboard_handlers = {
        show_note_dot(event) {
        /*  Add listeners to each fret, when hover on it by the mouse
            change opacity, so a note of the fret will be visible
        */  
            // Check if show all notes is selected
            if (show_all_notes) {
                return;
            }
            if (event.target.classList.contains('fret-note')) {
                if (show_duplicate_notes) {
                    fretboard_app.toggle_duplicate_notes(event.target.getAttribute('note-data'), 1);
                } else {
                    event.target.style.setProperty('--note-dot-opacity', 1);
                }
            }
        },

        hide_note_dot(event) {
        /*  When mouse out from the fret, change it opactity
            to zero
        */
            // Check if show all notes is selected
            if (show_all_notes) {
                return;
            }
            if (show_duplicate_notes) {
                fretboard_app.toggle_duplicate_notes(event.target.getAttribute('note-data'), 0);
            } else {
                event.target.style.setProperty('--note-dot-opacity', 0);
            }
        },

        set_selected_instrument(event) {
        /*  Whe user switch instrument options,
            change number of strings value, based on an instrument  
        */
            selected_instrument = event.target.value;
            number_of_strings = instrument_tuning_presets[selected_instrument].length;
            fretboard_app.setup_fretboard();
        },

        set_accidentals(event) {
        /*  Whe user switch accidental options, 
            change a type of notes notation (flats or sharps)
        */
            if (event.target.classList.contains('acc-select')) {
                accidentals = event.target.value;
                fretboard_app.setup_fretboard();
                fretboard_app.setup_note_name_section();
            } else {
                return;
            }
        },

        set_number_of_frets(event) {
        // Add listener to input number,
        // that change number of rendered frets of an instrument
            number_of_frets = number_of_frets_selector.value;
            fretboard_app.setup_fretboard();
        },
        
        set_show_all_notes() {
            // Set notes opacity to 1(visible) if 
            // show all notes selected
            show_all_notes = show_all_notes_selector.checked;
            if (show_all_notes_selector.checked) {
                root.style.setProperty('--note-dot-opacity', 1);
                fretboard_app.setup_fretboard();
            // If show all notes not selected
            } else {
                root.style.setProperty('--note-dot-opacity', 0);
                fretboard_app.setup_fretboard();
            }
        },
        set_show_duplicate_notes() {
        /* Realization of a toggle event on the checkbox */
            show_duplicate_notes = !show_duplicate_notes;
        },
        set_notes_to_show(event) {
            let note_to_show = event.target.innerText.split(" ");
            note_to_show.forEach(note => fretboard_app.toggle_duplicate_notes(note, 1));
        },
        set_notes_to_hide(event) {
            if (!show_all_notes_selector.checked) {
                let note_to_hide = event.target.innerText.split(" ");
                note_to_hide.forEach(note => fretboard_app.toggle_duplicate_notes(note, 0));
            } else {
                return;
            }
        },
        set_show_guitar_fretboard() {
            show_guitar_fretboard = show_guitar_fretboard_selector.checked
            if (!show_guitar_fretboard_selector.checked) {
                guitar_fretboard_container.style.setProperty('display', 'none');
                fretboard.style.setProperty('display', 'none');
                note_name_section.style.setProperty('display', 'none');
                chord_name_section.style.setProperty('display', 'none');
            } else {
                guitar_fretboard_container.style.removeProperty('display');
                fretboard.style.removeProperty('display');
                note_name_section.style.removeProperty('display');
                chord_name_section.style.removeProperty('display');
            }
        },
        set_show_metronome(){
            show_metronome = show_metronome_selector.checked
            if (!show_metronome_selector.checked) {
                metronome_container.style.setProperty('display', 'none')
            } else {
                metronome_container.style.removeProperty('display')
            }
        },
        set_show_interval_listener(){
            show_interval_listener = show_interval_listener_selector.checked
            if (!show_interval_listener_selector.checked) {
                interval_container.style.setProperty('display', 'none');
            } else {
                interval_container.style.removeProperty('display');
            }
        },
        setup_event_listeners() {

            fretboard.addEventListener('mouseover', this.show_note_dot);
            fretboard.addEventListener('mouseout', this.hide_note_dot);
            instrument_selector.addEventListener('change', this.set_selected_instrument);
            accidentals_selector.addEventListener('click', this.set_accidentals);
            number_of_frets_selector.addEventListener('change', this.set_number_of_frets);
            show_all_notes_selector.addEventListener('change', this.set_show_all_notes);
            show_duplicate_notes_selector.addEventListener('change', this.set_show_duplicate_notes);
            note_name_section.addEventListener('mouseover', this.set_notes_to_show);
            note_name_section.addEventListener('mouseout', this.set_notes_to_hide);
            chord_section.forEach(element => {
                element.addEventListener('mouseover', this.set_notes_to_show);
                element.addEventListener('mouseout', this.set_notes_to_hide);
            });
            show_metronome_selector.addEventListener('change', this.set_show_metronome);
            show_guitar_fretboard_selector.addEventListener('change', this.set_show_guitar_fretboard);
            show_interval_listener_selector.addEventListener('change', this.set_show_interval_listener);
           /*  test.addEventListener('mouseover', this.set_notes_to_show);
            test.addEventListener('mouseout', this.set_notes_to_hide); */
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
})();

