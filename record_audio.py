# import required libraries
import sounddevice as sd
from scipy.io.wavfile import write
  
# Sampling frequency
freq = 16000
  
# Recording duration
duration = 5
  
# Start recorder with the given values 
# of duration and sample frequency
recording = sd.rec(int(duration * freq), 
                   samplerate=freq, channels=2)
  
# Record audio for the given number of seconds
sd.wait()

# This will convert the NumPy array to an audio
# file with the given sampling frequency
write("name.wav", freq, recording)