import threading
import queue
import numpy as np
import soundcard as sc
import soundfile as sf

OUTPUT_FILE_NAME = "out.wav"  # file name.
SAMPLE_RATE = 48000  # [Hz]. sampling rate.
RECORD_SEC = 10  # [sec]. duration recording audio.

# Queue to store recorded audio data
audio_queue = queue.Queue()

# Function to record audio from the microphone
def record_microphone():
    with sc.default_microphone().recorder(samplerate=SAMPLE_RATE) as mic:
        mic_data = mic.record(numframes=SAMPLE_RATE * RECORD_SEC)
    audio_queue.put(("mic", mic_data))

# Function to record audio with loopback from default speaker
def record_loopback():
    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as spk:
        spk_data = spk.record(numframes=SAMPLE_RATE * RECORD_SEC)
    audio_queue.put(("spk", spk_data))

# Create and start threads for recording microphone and loopback audio
mic_thread = threading.Thread(target=record_microphone)
spk_thread = threading.Thread(target=record_loopback)
mic_thread.start()
spk_thread.start()

# Wait for both threads to finish
mic_thread.join()
spk_thread.join()

# Process and combine the recorded audio data based on time
combined_data = []
while not audio_queue.empty():
    source, data = audio_queue.get()
    if len(combined_data) == 0:
        combined_data = data
    else:
        combined_data = np.concatenate((combined_data, data), axis=1)

# Save the combined audio data to a WAV file
sf.write(file=OUTPUT_FILE_NAME, data=combined_data, samplerate=SAMPLE_RATE)
