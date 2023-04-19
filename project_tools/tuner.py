import numpy as np
import wave
import struct

ALL_NOTES = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
CONCERT_PITCH = 440
GUITAR_FREQ_RANGE = [40, 400]
PIANO_FREQ_RANGE = [27.5, 4190]


def note_range(instrument_type: str = None):
	instrument_range = {
		'guitar': GUITAR_FREQ_RANGE,
		'piano': PIANO_FREQ_RANGE
	}
	def note_range_decorator(func):
		def cut_freq(*args, **kwargs):
				frequency = func(*args, **kwargs)
				min_freq = min(instrument_range.get(instrument_type))
				max_freq = max(instrument_range.get(instrument_type))
				return frequency if min_freq < frequency < max_freq else None
		return cut_freq
	return note_range_decorator


@note_range('guitar')
def find_max_frequency(audio_file):
	# Get the number of frames in the audio file
    file_length = audio_file.getnframes()

    # Get the sampling frequency of the audio file
    sampling_frequency = audio_file.getframerate()

    # Read the audio file as a numpy array
    sound = np.frombuffer(audio_file.readframes(file_length), dtype=np.int16)

    # Normalize the sound array to the range [-1, 1]
    sound = sound / np.iinfo(np.int16).max

    # Compute the length of the Hamming window
    window_length = min(file_length, 13128)

    # Create a Hamming window of the appropriate length
    window = np.hamming(window_length)

    # Apply the Hamming window to the sound array
    sound = sound[:window_length] * window

    # Compute the one-dimensional discrete Fourier Transform
    fourier = np.fft.fft(sound)

    # Compute the magnitude spectrum of the Fourier Transform
    magnitude_spectrum = np.abs(fourier)

    # Find the index of the maximum value in the magnitude spectrum
    max_index = np.argmax(magnitude_spectrum[:window_length // 2])

    # Compute the frequency corresponding to the maximum value
    frequency = max_index * sampling_frequency / window_length

    return round(frequency, 1)


def get_closest_note(pitch: float):
    """
    Function finds the closest note
    for a given pitch(Hz)
    """

    i = int(np.round(np.log2(pitch/CONCERT_PITCH)*12))
    closest_note = ALL_NOTES[i%12] # + str(4 + (i + 9) // 12)
    closest_pitch = CONCERT_PITCH*2**(i / 12)
    return closest_note, round(closest_pitch, 1)


if __name__ == "__main__":
	pass