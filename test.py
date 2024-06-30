import time
from typing import List

import comtypes
from ctypes import windll

# Initialize COM
windll.ole32.CoInitializeEx(None, comtypes.CLSCTX_ALL)
import datetime
import threading
import queue
import numpy as np
import soundcard as sc
import soundfile as sf

# Initialize COM
windll.ole32.CoInitializeEx(None, comtypes.CLSCTX_ALL)

from src.MicrophoneDetectionService import microphone_is_on, microphone_is_on_and_talking, stopped_talking, \
    mute_microphone, unmute_microphone

RECORD_SEC = 1
CHUNK_SIZE = 1024  # Number of frames per chunk
BUFFER_SECONDS = 0.1  # Buffer size in seconds
SAMPLE_RATE = 44100  # Standard sample rate, adjust as needed
# Queue to store recorded audio data
global audio_queue
audio_queue = queue.PriorityQueue()
global threads_running

threads_running = False


def record_microphone():
    global threads_running
    global audio_queue

    try:
        with sc.default_microphone().recorder(samplerate=SAMPLE_RATE) as mic:
            while threads_running:
                mic_data = mic.record(numframes=SAMPLE_RATE * RECORD_SEC)
                audio_queue.put((datetime.datetime.now(), "mic", mic_data))
                # remaining_data = mic.flush()
                # audio_queue.put((datetime.datetime.now(), "mic", remaining_data))

                # print("Recording from microphone...")
                # time.sleep(BUFFER_SECONDS)  # Small delay to prevent overwhelming the CPU

    except Exception as e:
        print(f"Error recording microphone: {e}")


def record_loopback():
    global threads_running
    global audio_queue

    try:
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(
                samplerate=SAMPLE_RATE) as spk:
            while threads_running:
                spk_data = spk.record(numframes=SAMPLE_RATE * RECORD_SEC)
                audio_queue.put((datetime.datetime.now(), "spk", spk_data))
                # remaining_data = spk.flush()
                # audio_queue.put((datetime.datetime.now(), "spk", remaining_data))
                # print("Recording from speaker loopback...")
    except Exception as e:
        print(f"Error recording loopback: {e}")


import numpy as np
from scipy import interpolate


def interpolate_audio(audio_data, target_length):
    x = np.arange(len(audio_data))
    x_new = np.linspace(0, len(audio_data) - 1, target_length)
    f = interpolate.interp1d(x, audio_data, kind='linear', axis=0, fill_value='extrapolate')
    return f(x_new)


def ensure_stereo(audio_data):
    if audio_data.ndim == 1:
        # If mono, duplicate the channel
        return np.column_stack((audio_data, audio_data))
    elif audio_data.shape[1] == 1:
        # If 2D but still mono, duplicate the channel
        return np.column_stack((audio_data, audio_data))
    elif audio_data.shape[1] == 2:
        # If already stereo, return as is
        return audio_data
    else:
        # If more than 2 channels, just take the first two
        return audio_data[:, :2]


def save_recording(audio_data: List):
    print("Entering Save Recording")
    if not (len(audio_data) > 0):
        return True

    # Sort the audio data based on timestamps
    sorted_audio = sorted(audio_data, key=lambda x: x[0])
    print("Sorted the audio")

    # Combine the audio data
    # combined_data = []
    # for _, source, data in sorted_audio:
    #     if len(combined_data) == 0:
    #         combined_data = data
    #     else:
    #         if combined_data.shape[1] < data.shape[1]:
    #             combined_data = np.hstack(
    #                 (combined_data, np.zeros((combined_data.shape[0], data.shape[1] - combined_data.shape[1]))))
    #         elif combined_data.shape[1] > data.shape[1]:
    #             data = np.hstack((data, np.zeros((data.shape[0], combined_data.shape[1] - data.shape[1]))))
    #         combined_data = np.vstack((combined_data, data))

    # In the save_recording function:
    max_length = max(data.shape[0] for _, _, data in sorted_audio)
    combined_data = []
    for _, source, data in sorted_audio:
        # Choose either ensure_stereo or ensure_mono based on your preference
        data = ensure_stereo(data)  # or ensure_mono(data)
        combined_data.append(data)

    combined_data = np.vstack(combined_data)

    if combined_data.size > 0:
        if combined_data.ndim == 1:
            combined_data = combined_data.reshape(-1, 1)
        filename = f"output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        sf.write(file=filename, data=combined_data, samplerate=SAMPLE_RATE)
        print(f"Saved recording to {filename}")


def start_recording():
    audio_data = []
    global audio_queue
    recording_threads = []
    global threads_running

    try:
        while True:
            if microphone_is_on():
                print("microphone is on")
                if not threads_running:
                    # Start the recording threads
                    mic_thread = threading.Thread(target=record_microphone)
                    spk_thread = threading.Thread(target=record_loopback)

                    mic_thread.start()
                    spk_thread.start()

                    recording_threads.extend([mic_thread, spk_thread]) #mic_thread
                    threads_running = True

                if stopped_talking():
                    print("Stopped talking")
                    threads_running = False
                    print("Microphone is off")

                    for thread in recording_threads:
                        print("About to join thread")

                        thread.join()

                    # Process and combine the recorded audio data
                    print("About to enter combined audio")
                    print(audio_queue)

                    while True:
                        try:
                            item = audio_queue.get_nowait()
                            audio_data.append(item)
                        except Exception as e:
                            print(e)
                            break
                    print("About to enter Saving recording")

                    save_recording(audio_data)

                    audio_data = []

                    recording_threads.clear()
                    threads_running = False


            else:
                print("microphone is off")

                if threads_running:
                    print("Threads are running")

                    # Wait for both threads to finish
                    for thread in recording_threads:
                        thread.join()

                    # Process and combine the recorded audio data
                    while audio_queue.qsize() > 0:
                        audio_data.append(audio_queue.get())

                    save_recording(audio_data)

                    audio_data = []

                    recording_threads.clear()
                    threads_running = False

                else:
                    print("No Threads running")

            print("Sleeping for 5 seconds")

            time.sleep(1)  # Check the microphone status every 5 seconds

    except Exception as e:
        print(e)
    finally:
        print("Final save before exit")
        save_recording(audio_data)  # Save any remaining data before exiting


start_recording()
# Uninitialize COM if necessary
# windll.ole32.CoUninitialize()
