import pyaudio

import pyaud
import numpy as np
from scipy.signal import find_peaks

# Define constants
FORMAT = pyaudio.paInt16  # Audio format (16-bit int)
CHANNELS = 1  # Number of audio channels (mono)
RATE = 44100  # Sampling rate (samples per second)
CHUNK = 1024  # Number of frames per buffer
MUSIC_THRESHOLD = 1000  # Threshold for detecting music


def detect_music(data):
    # Convert raw data to numpy array
    audio_data = np.frombuffer(data, dtype=np.int16)

    # Perform a Fourier transform to get the frequency spectrum
    spectrum = np.fft.fft(audio_data)
    spectrum = np.abs(spectrum[:len(spectrum) // 2])  # Take the positive frequencies

    # Find peaks in the spectrum
    peaks, _ = find_peaks(spectrum, height=MUSIC_THRESHOLD)

    # Simple heuristic: if we have multiple peaks, it's likely music
    if len(peaks) > 20:
        print(len(peaks))
        return True
    return False


# Initialize PyAudio
p = pyaudio.PyAudio()

# Open a stream to capture audio
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                # input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("Listening for music...")

while True:
    try:
        # Read a chunk of audio data
        data = stream.read(CHUNK)

        # Check if music is detected
        if detect_music(data):
            print("Music detected!")
    except Exception as e:
        print(e)
        print("Exiting...")


# Clean up
stream.stop_stream()
stream.close()
p.terminate()
