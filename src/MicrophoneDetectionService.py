from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, IAudioMeterInformation
import time


def microphone_is_on():
    try:
        devices = AudioUtilities.GetMicrophone()
        print(devices)
    except Exception as e:
        print("No default devices found: " + e.__str__())
    else:
        interface = devices.Activate(
            IAudioMeterInformation._iid_, CLSCTX_ALL, None)
        meter_info = cast(interface, POINTER(IAudioMeterInformation))

        try:
            peak_value = meter_info.GetPeakValue()
            # print(f"Current Speaker Peak Value: {peak_value * 100:.2f}%")
            if peak_value * 100 > 0.1:
                print(f"Current Microphone Peak Value: {peak_value * 100:.2f}%")
                return True
        except Exception as e:
            print(f"Error retrieving peak value: {e}")
    finally:
        return False


if __name__ == '__main__':
    while True:
        microphone_is_on()
        time.sleep(1)
