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
	# Storing our sound file as a numpy array
	file_length = audio_file.getnframes() 
	#sampling frequency
	sampling_frequency = audio_file.getframerate() 
	# blank array
	sound = np.zeros(file_length) 

	for i in range(file_length) : 
		wdata = audio_file.readframes(1)
		data = struct.unpack("q",wdata)
		sound[i] = int(data[0])
	# scaling it to 0 - 1
	sound=np.divide(sound,float(2**15)) 

	#number of channels mono/sterio
	counter = audio_file.getnchannels()

	#fourier transformation from numpy module
	fourier = np.fft.fft(sound)
	fourier = np.absolute(fourier)
	imax=np.argmax(fourier[0:int(file_length/2)]) #index of max element

	#peak detection
	i_begin = -1
	threshold = 0.3 * fourier[imax]
	for i in range (0,imax+100):
		if fourier[i] >= threshold:
			if(i_begin == -1):
				i_begin = i				
		if(i_begin !=-1 and fourier[i] < threshold):
			break
	i_end = i
	imax = np.argmax(fourier[0:i_end+100])
	
	#formula to convert index into sound frequency
	freq=(imax*sampling_frequency)/(file_length*counter) 
	
	return round(freq, 1)

def get_closest_note(pitch: float):
    """
    Function finds the closest note
    for a given pitch(Hz)
    """

    i = int(np.round(np.log2(pitch/CONCERT_PITCH)*12))
    closest_note = ALL_NOTES[i%12] # + str(4 + (i + 9) // 12)
    closest_pitch = CONCERT_PITCH*2**(i / 12)
    return closest_note#, round(closest_pitch, 1)


if __name__ == "__main__":
	pass