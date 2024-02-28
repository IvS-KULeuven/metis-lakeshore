from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
from PySide6.QtCore import QTimer
import serial
import serial.tools.list_ports
from ui.left_ui import LeftUI
from ui.temperature_ui import TemperatureUI
from serialcom.general import read_general_information, read_brightness, handle_module_name_change, handle_brightness_change, handle_restore_factory_settings
from serialcom.profibus import read_address, read_slot_count, read_slots, handle_address_change, handle_slot_count_change, profibus_connect_combobox
from serialcom.sensor import read_input_names, read_sensor_setup, sensor_connect_type_combobox, sensor_connect_name_edit, sensor_connect_power_combobox, sensor_connect_combobox
from serialcom.curve import read_curves, curve_connect_delete_button, curve_connect_curve_combobox
from serialcom.temperature import read_temperature, read_sensor_units
from serialcom.connect import find_connected_devices, handle_disconnect

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create QHBoxlayout for the application, it will be split into a left and right part
        self.layout = QHBoxLayout(self)

        # Create instances of imported UI's
        self.left_ui = LeftUI()
        self.temperature_ui = TemperatureUI()

        # Add left and right layouts to main layoutd
        self.layout.addLayout(self.left_ui.layout)
        self.layout.addLayout(self.temperature_ui.vlayout)

        # Access attributes from instances of LeftUI
        self.general_ui = self.left_ui.general_ui
        self.connection_ui = self.left_ui.connection_ui
        self.profibus_ui = self.left_ui.profibus_ui
        self.curve_ui = self.left_ui.curve_ui
        self.sensor_ui = self.left_ui.sensor_ui

        # Create variables to store serial information
        self.port = ''
        self.baudrate = 115200
        self.timeout = 1
        self.ser = ''

        # Connect connect, disconnect and refresh buttons
        self.connection_ui.connect_button.clicked.connect(self.handle_connect)
        self.connection_ui.disconnect_button.clicked.connect(lambda: handle_disconnect(self))
        self.connection_ui.refresh_button.clicked.connect(lambda: find_connected_devices(self))

        # Call the function to search for connected devices
        find_connected_devices(self)

        # Create the timers
        self.temp_timer = QTimer(self)
        self.temp_timer.setInterval(10000)  # Update every 10 seconds
        self.temp_timer.timeout.connect(lambda: read_temperature(self))
        self.sensor_timer = QTimer(self)
        self.sensor_timer.setInterval(10000)  # Update every 10 seconds
        self.sensor_timer.timeout.connect(lambda: read_sensor_units(self))

    
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
    

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
