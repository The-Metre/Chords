const tempo_display = document.querySelector('.tempo');
const tempo_text = document.querySelector('.tempo-text');
const decrease_tempo_button = document.querySelector('.decrease-tempo');
const increase_tempo_button = document.querySelector('.increase-tempo');
const tempo_slider = document.querySelector('.tempo-slider');
const metronome_stop_button = document.querySelector('.metronome-start-stop-button');
const subtract_beats = document.querySelector('.subtract-beats');
const add_beats = document.querySelector('.add-beats');
const measure_count = document.querySelector('.measure-count');

let bpm = 140;
let beats_per_measure = 4;
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
});

add_beats.addEventListener('click', () => {
    if (beats_per_measure >= 12) { return }
    beats_per_measure++;
    measure_count.textContent = beats_per_measure;
});

function update_metronome() {
    tempo_display.textContent = bpm;
    tempo_slider.value = bpm;
    tempo_text.textContent = tempo_text_string

}

function validate_tempo() {
    if (bpm <= 20) { return };
    if (bpm >= 280) { return };
}