from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioMeterInformation
import time


def get_speaker_output():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioMeterInformation._iid_, CLSCTX_ALL, None)
    meter_info = cast(interface, POINTER(IAudioMeterInformation))

    try:
        peak_value = meter_info.GetPeakValue()
        print(f"Current Speaker Peak Value: {peak_value * 100:.2f}%")
    except Exception as e:
        print(f"Error retrieving peak value: {e}")


def get_microphone_output():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioMeterInformation._iid_, CLSCTX_ALL, None)
    meter_info = cast(interface, POINTER(IAudioMeterInformation))

    try:
        peak_value = meter_info.GetPeakValue()
        print(f"Current Speaker Peak Value: {peak_value * 100:.2f}%")
    except Exception as e:
        print(f"Error retrieving peak value: {e}")


def monitor_speaker_output():
    while True:
        get_speaker_output()
        time.sleep(1)  # Wait for 1 second before checking again


if __name__ == "__main__":
    monitor_speaker_output()
