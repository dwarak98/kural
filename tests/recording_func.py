import wave
import pyaudio
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

# Define the duration of recording in seconds
duration = 10  # You can adjust this as needed

# Set the sample rate (44100 Hz is a common value)
sample_rate = 44100

# Set the file name for saving the recording
file_name = "speaker_recording.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Get the default input and output devices
input_device = audio.get_default_input_device_info()
output_device = audio.get_default_output_device_info()

# Open the microphone stream
# mic_stream = audio.open(format=pyaudio.paInt16,
#                         channels=1,
#                         rate=sample_rate,
#                         input=True,
#                         input_device_index=1,
#                         frames_per_buffer=1024)

# Open the speaker stream
speaker_stream = audio.open(format=pyaudio.paInt16,
                            channels=2,
                            rate=sample_rate,
                            output=True,
                            output_device_index=4)

# Create a wave file for saving the recording
wave_file = wave.open(file_name, 'wb')
wave_file.setnchannels(1)
wave_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
wave_file.setframerate(sample_rate)

# Record microphone input and speaker output simultaneously
print("Recording...")

# Record and save the audio
for _ in range(int(duration * sample_rate / 1024)):
    # mic_data = mic_stream.read(1024)
    speaker_data = speaker_stream.read(1024)
    # wave_file.writeframes(mic_data)
    wave_file.writeframes(speaker_data)

# Close the streams and save the file
wave_file.close()
# mic_stream.stop_stream()
# mic_stream.close()
speaker_stream.stop_stream()
speaker_stream.close()
audio.terminate()

print(f"Recording saved as {file_name}")
