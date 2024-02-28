import serial
import serial.tools.list_ports

def find_connected_devices(main_window):
        # Clear stuff
        main_window.connection_ui.connection_combobox.clear()
        main_window.connection_ui.devices_list.clear()
        
        # Scan USB ports for connected devices
        devices = serial.tools.list_ports.comports()

        # Add devices to the combobox
        for device in devices:
            with serial.Serial(device.device) as ser:
                device_str = remove_duplicate_parts(str(device))
                main_window.connection_ui.connection_combobox.addItem(device_str)
                main_window.connection_ui.devices_list.append(device)

def remove_duplicate_parts(input_string):
    parts = input_string.split(" - ")
    if len(parts) == 3 and parts[1] == parts[2]:
        return parts[0] + " - " + parts[1]
    else:
        return input_string