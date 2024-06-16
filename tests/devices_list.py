import pyaudio

audio = pyaudio.PyAudio()

for i in range(audio.get_device_count()):
    device_info = audio.get_device_info_by_index(i)
    print(f"Device {i}: {device_info['name']}, {device_info['hostApi']}, {device_info['maxInputChannels']}, {device_info['maxOutputChannels']}")
