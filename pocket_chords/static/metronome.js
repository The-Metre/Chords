import Timer from './timer.js';

(function() {

    const tempo_display = document.querySelector('.tempo');
    const tempo_text = document.querySelector('.tempo-text');
    const decrease_tempo_button = document.querySelector('.decrease-tempo');
    const increase_tempo_button = document.querySelector('.increase-tempo');
    const tempo_slider = document.querySelector('.tempo-slider');
    const metronome_stop_button = document.querySelector('.metronome-start-stop-button');
    const subtract_beats = document.querySelector('.subtract-beats');
    const add_beats = document.querySelector('.add-beats');
    const measure_count = document.querySelector('.measure-count');


    const click1 = new Audio('http://127.0.0.1:8000/static/click1.mp3');
    const click2 = new Audio('http://127.0.0.1:8000/static/click2.mp3');

    let bpm = 140;
    let beats_per_measure = 4;
    let is_running = false;
    let count = 0;
    let tempo_text_string = 'Medium';



    decrease_tempo_button.addEventListener('click', () => {
        bpm--;
        validate_tempo();
        update_metronome();
    });

    increase_tempo_button.addEventListener('click', () => {
        bpm++;
        validate_tempo();
        update_metronome();
    });

    tempo_slider.addEventListener('input', () => {
        bpm = tempo_slider.value;
        validate_tempo();
        update_metronome();
    });

    subtract_beats.addEventListener('click', () => {
        if (beats_per_measure <= 2) { return }
        beats_per_measure--;
        measure_count.textContent = beats_per_measure;
        count = 0;
    });

    add_beats.addEventListener('click', () => {
        if (beats_per_measure >= 12) { return }
        beats_per_measure++;
        measure_count.textContent = beats_per_measure;
        count = 0;
    });

    metronome_stop_button.addEventListener('click', () => {
        count = 0;
        if (!is_running) {
            metronome.start();
            is_running = true;
            metronome_stop_button.textContent = "STOP"; 
        } else {
            metronome.stop();
            is_running = false;
            metronome_stop_button.textContent = "START";
        }
    });

    function update_metronome() {
        tempo_display.textContent = bpm;
        tempo_slider.value = bpm;
        metronome.timeInterval = 60000 / bpm;
        tempo_text.textContent = tempo_text_string;

    };

    function validate_tempo() {
        if (bpm <= 20) { return };
        if (bpm >= 280) { return };
    }

    function play_click() {
        console.log(count)
        if (count === beats_per_measure) {
            count = 0;
        }
        if (count == 0) {
            click1.play();
            click1.currentTime = 0;
        } else {
            click2.play();
            click2.currentTime = 0;
        }
        count++;
    }

    const metronome = new Timer(play_click, 60000 / bpm, { immediate: true });

})();