import sounddevice as sd
import numpy as np

def detect_speaker_status(duration=10, threshold=2, sample_rate=44100):
    """
    Detect if the speaker is on or off based on audio output.

    Parameters:
    - duration: Duration in seconds to sample audio.
    - threshold: Amplitude threshold to determine if the speaker is on.
    - sample_rate: Sampling rate of the audio device.

    Returns:
    - bool: True if speaker is on, False otherwise.
    """

    def callback(indata, frames, time, status):
        # This callback will be called for each audio block.
        volume_norm = np.linalg.norm(indata) * 10
        print(volume_norm)

        if volume_norm > threshold:
            print(volume_norm)
            callback.detected = True

    # Initialize callback attribute
    callback.detected = False

    # Start recording audio from the default output device
    with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate, device=0):
        sd.sleep(duration * 1000)

    return callback.detected


# Example usage:
if detect_speaker_status():
    print("Speaker is on")
else:
    print("Speaker is off")


def list_audio_devices():
    print(sd.query_devices())


# List available audio devices
list_audio_devices()
