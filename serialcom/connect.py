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

def handle_connect(self):
        i = self.connection_ui.connection_combobox.currentIndex()
        device = self.connection_ui.devices_list[i]
        self.port = device.device
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        read_general_information(self)
        read_brightness(self)
        read_input_names(self)
        read_address(self)
        read_slot_count(self)
        read_slots(self)
        read_sensor_setup(self)
        read_curves(self)
        read_sensor_units(self)
        read_temperature(self)

        # Connect signals
        self.general_ui.module_name_label.editingFinished.connect(lambda: handle_module_name_change(self))
        self.profibus_ui.address_line_edit.editingFinished.connect(lambda: handle_address_change(self))
        self.general_ui.brightness_combobox.currentIndexChanged.connect(lambda: handle_brightness_change(self))
        self.profibus_ui.slot_combobox.currentIndexChanged.connect(lambda: handle_slot_count_change(self))
        self.general_ui.restore_button.clicked.connect(lambda: handle_restore_factory_settings(self))
        # Connect signals for comboboxes and others
        for i in range(8):
            profibus_connect_combobox(self.profibus_ui.channel_comboboxes[i],self, i)
            profibus_connect_combobox(self.profibus_ui.units_comboboxes[i],self, i)
            sensor_connect_type_combobox(self.sensor_ui.type_comboboxes[i], self, i)
            sensor_connect_power_combobox(self.sensor_ui.power_comboboxes[i], self, i)
            sensor_connect_name_edit(self.sensor_ui.name_line_edits[i], self, i)
            sensor_connect_name_edit(self.curve_ui.name_labels[i], self, i)
            sensor_connect_combobox(self.sensor_ui.current_reversal_comboboxes[i], self, i)
            sensor_connect_combobox(self.sensor_ui.autorange_comboboxes[i], self, i)
            sensor_connect_combobox(self.sensor_ui.range_comboboxes[i], self, i)
            sensor_connect_combobox(self.sensor_ui.display_units_comboboxes[i], self, i)
            curve_connect_delete_button(self.curve_ui.delete_buttons[i], self, i)
            curve_connect_curve_combobox(self.curve_ui.curve_comboboxes[i], self, i)
        
        # start_timers()
        self.temp_timer.start()
        self.sensor_timer.start()

        self.connection_ui.status_label.setText("<b>Status: </b>        Connected")