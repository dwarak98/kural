from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, IAudioMeterInformation
import time
import psutil


def mute_microphone():
    try:
        # Get the default audio endpoint (microphone)
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)

        # Mute the microphone
        volume.SetMute(True, None)
        print("Microphone muted.")
        return True
    except Exception as e:
        print("Error muting microphone:", e)
        return False


def stopped_talking():
    peak_values = []
    for i in range(30):
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
                if peak_value * 100 > 1:
                    print(f"Current Microphone Peak Value: {peak_value * 100:.2f}%")
                    peak_values.append(False)
                    return False

                else:
                    print(f"Current Microphone Peak Value: {peak_value * 100:.2f}%")
                    peak_values.append(True)
            except Exception as e:
                print(f"Error retrieving peak value: {e}")
        time.sleep(1)

    if False in peak_values:
        return False
    else:
        return True


def microphone_is_on_and_talking():
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
            if peak_value * 100 > 0.2:
                print(f"Current Microphone Peak Value: {peak_value * 100:.2f}%")
                return True

            else:
                print(f"Current Microphone Peak Value: {peak_value * 100:.2f}%")
                return False
        except Exception as e:
            print(f"Error retrieving peak value: {e}")

def unmute_microphone():
    try:
        # Get the default audio endpoint (microphone)
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)

        # Unmute the microphone
        volume.SetMute(False, None)
        print("Microphone unmuted.")
        return True
    except Exception as e:
        print("Error unmuting microphone:", e)
        return False

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
            if peak_value * 100 > 0.0:
                print(f"Current Microphone Peak Value: {peak_value * 100:.2f}%")
                return True

            else:
                print(f"Current Microphone Peak Value: {peak_value * 100:.2f}%")
                return False
        except Exception as e:
            print(f"Error retrieving peak value: {e}")


def get_process_name(pid):
    try:
        return psutil.Process(pid).name()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return "Unknown"


def list_active_microphone_sessions():
    sessions = AudioUtilities.GetAllSessions()
    print(sessions)
    for session in sessions:
        if session.Process and session.is_active():
            process_id = session.ProcessId
            process_name = get_process_name(process_id)
            print(f"Active session: {process_name} (PID: {process_id})")


if __name__ == '__main__':
    while True:
        variable = microphone_is_on()
        if variable:
            mute_microphone()
        # print(variable)
        time.sleep(1)
