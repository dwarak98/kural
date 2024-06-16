from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, IAudioMeterInformation
import time


def get_microphone_peak():
    try:
        devices = AudioUtilities.GetMicrophone()
        print(devices)
    except Exception as e:
        print("No default devices found: "+e.__str__())
    else:
        interface = devices.Activate(
            IAudioMeterInformation._iid_, CLSCTX_ALL, None)
        meter_info = cast(interface, POINTER(IAudioMeterInformation))

        try:
            peak_value = meter_info.GetPeakValue()
            print(f"Current Microphone Peak Value: {peak_value * 100:.2f}%")
        except Exception as e:
            print(f"Error retrieving peak value: {e}")


def monitor_microphone_peak():
    while True:
        get_microphone_peak()
        time.sleep(1)  # Wait for 1 second before checking again


if __name__ == "__main__":
    monitor_microphone_peak()
