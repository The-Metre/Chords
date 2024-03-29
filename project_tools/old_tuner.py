import numpy as np
import wave
import struct

def old_max_freq(audio_file):
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