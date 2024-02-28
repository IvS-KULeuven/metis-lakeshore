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


def handle_disconnect(main_window):
    if main_window.ser == '':
        return
    try:
        main_window.ser.close()
        main_window.temp_timer.stop()
        main_window.sensor_timer.stop()
        
        # Disconnect signals
        main_window.general_ui.module_name_label.editingFinished.disconnect()
        main_window.profibus_ui.address_line_edit.editingFinished.disconnect()
        main_window.general_ui.brightness_combobox.currentIndexChanged.disconnect()
        main_window.profibus_ui.slot_combobox.currentIndexChanged.disconnect()
        main_window.general_ui.restore_button.clicked.disconnect()

        # Disconnect signals for comboboxes and others
        for i in range(8):
            main_window.profibus_ui.channel_comboboxes[i].currentIndexChanged.disconnect()
            main_window.profibus_ui.units_comboboxes[i].currentIndexChanged.disconnect()
            main_window.sensor_ui.type_comboboxes[i].currentIndexChanged.disconnect()
            main_window.sensor_ui.power_comboboxes[i].currentIndexChanged.disconnect()
            main_window.sensor_ui.name_line_edits[i].editingFinished.disconnect()
            main_window.curve_ui.name_labels[i].editingFinished.disconnect()
            main_window.sensor_ui.current_reversal_comboboxes[i].currentIndexChanged.disconnect()
            main_window.sensor_ui.autorange_comboboxes[i].currentIndexChanged.disconnect()
            main_window.sensor_ui.range_comboboxes[i].currentIndexChanged.disconnect()
            main_window.sensor_ui.display_units_comboboxes[i].currentIndexChanged.disconnect()
            main_window.curve_ui.delete_buttons[i].clicked.disconnect()
            main_window.curve_ui.curve_comboboxes[i].currentIndexChanged.disconnect()

        main_window.connection_ui.status_label.setText("<b>Status: </b>        Disconnected")
    except Exception as e:
        print(f"Error: {e}")