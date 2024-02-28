import serial
import serial.tools.list_ports
from serialcom.general import read_general_information, read_brightness, handle_module_name_change, handle_brightness_change, handle_restore_factory_settings
from serialcom.profibus import read_address, read_slot_count, read_slots, handle_address_change, handle_slot_count_change, profibus_connect_combobox
from serialcom.sensor import read_input_names, read_sensor_setup, sensor_connect_type_combobox, sensor_connect_name_edit, sensor_connect_power_combobox, sensor_connect_combobox
from serialcom.curve import read_curves, curve_connect_delete_button, curve_connect_curve_combobox
from serialcom.temperature import read_temperature, read_sensor_units

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

def handle_connect(main_window):
        i = main_window.connection_ui.connection_combobox.currentIndex()
        device = main_window.connection_ui.devices_list[i]
        main_window.port = device.device
        main_window.ser = serial.Serial(main_window.port, main_window.baudrate, timeout=main_window.timeout)
        read_general_information(main_window)
        read_brightness(main_window)
        read_input_names(main_window)
        read_address(main_window)
        read_slot_count(main_window)
        read_slots(main_window)
        read_sensor_setup(main_window)
        read_curves(main_window)
        read_sensor_units(main_window)
        read_temperature(main_window)

def connect_signals(main_window):
    # Connect signals
    main_window.general_ui.module_name_label.editingFinished.connect(lambda: handle_module_name_change(main_window))
    main_window.profibus_ui.address_line_edit.editingFinished.connect(lambda: handle_address_change(main_window))
    main_window.general_ui.brightness_combobox.currentIndexChanged.connect(lambda: handle_brightness_change(main_window))
    main_window.profibus_ui.slot_combobox.currentIndexChanged.connect(lambda: handle_slot_count_change(main_window))
    main_window.general_ui.restore_button.clicked.connect(lambda: handle_restore_factory_settings(main_window))
    
    # Connect signals for comboboxes and others
    for i in range(8):
        profibus_connect_combobox(main_window.profibus_ui.channel_comboboxes[i],main_window, i)
        profibus_connect_combobox(main_window.profibus_ui.units_comboboxes[i],main_window, i)
        sensor_connect_type_combobox(main_window.sensor_ui.type_comboboxes[i], main_window, i)
        sensor_connect_power_combobox(main_window.sensor_ui.power_comboboxes[i], main_window, i)
        sensor_connect_name_edit(main_window.sensor_ui.name_line_edits[i], main_window, i)
        sensor_connect_name_edit(main_window.curve_ui.name_labels[i], main_window, i)
        sensor_connect_combobox(main_window.sensor_ui.current_reversal_comboboxes[i], main_window, i)
        sensor_connect_combobox(main_window.sensor_ui.autorange_comboboxes[i], main_window, i)
        sensor_connect_combobox(main_window.sensor_ui.range_comboboxes[i], main_window, i)
        sensor_connect_combobox(main_window.sensor_ui.display_units_comboboxes[i], main_window, i)
        curve_connect_delete_button(main_window.curve_ui.delete_buttons[i], main_window, i)
        curve_connect_curve_combobox(main_window.curve_ui.curve_comboboxes[i], main_window, i)
   

    # start_timers()
    main_window.temp_timer.start()
    main_window.sensor_timer.start()

    main_window.connection_ui.status_label.setText("<b>Status: </b>        Connected")