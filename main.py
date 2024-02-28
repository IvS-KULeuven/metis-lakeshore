from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QTableWidgetItem
from PySide6.QtCore import QTimer
import serial
import serial.tools.list_ports
from ui.left_ui import LeftUI
from ui.temperature_ui import TemperatureUI
from serialcom.general import read_general_information, read_brightness, handle_module_name_change, handle_brightness_change, handle_restore_factory_settings
from serialcom.profibus import read_address, read_slot_count, read_slots, handle_address_change, handle_slot_count_change, profibus_connect_combobox
from serialcom.sensor import read_input_names, read_sensor_setup, sensor_connect_type_combobox, sensor_connect_name_edit, sensor_connect_power_combobox, sensor_connect_combobox
from serialcom.curve import read_curves
from serialcom.temperature import read_temperature, read_sensor_units

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
        self.connection_ui.disconnect_button.clicked.connect(self.handle_disconnect)
        self.connection_ui.refresh_button.clicked.connect(self.find_connected_devices)

        # Call the function to search for connected devices
        self.find_connected_devices()

        # Create the timers
        self.temp_timer = QTimer(self)
        self.temp_timer.setInterval(10000)  # Update every 10 seconds
        self.temp_timer.timeout.connect(lambda: read_temperature(self))
        self.sensor_timer = QTimer(self)
        self.sensor_timer.setInterval(10000)  # Update every 10 seconds
        self.sensor_timer.timeout.connect(lambda: read_sensor_units(self))

    def find_connected_devices(self):
        # Clear stuff
        self.connection_ui.connection_combobox.clear()
        self.connection_ui.devices_list.clear()
        
        # Scan USB ports for connected devices
        devices = serial.tools.list_ports.comports()

        # Add devices to the combobox
        for device in devices:
            with serial.Serial(device.device) as ser:
                device_str = self.remove_duplicate_parts(str(device))
                self.connection_ui.connection_combobox.addItem(device_str)
                self.connection_ui.devices_list.append(device)

    def remove_duplicate_parts(self, input_string):
        parts = input_string.split(" - ")
        if len(parts) == 3 and parts[1] == parts[2]:
            return parts[0] + " - " + parts[1]
        else:
            return input_string
                
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
            self.curve_ui.delete_buttons[i].clicked.connect(self.handle_delete_curve)
            self.curve_ui.curve_comboboxes[i].currentIndexChanged.connect(self.handle_curve_change)
        
        # start_timers()
        self.temp_timer.start()
        self.sensor_timer.start()

        self.connection_ui.status_label.setText("<b>Status: </b>        Connected")
    
    def handle_disconnect(self):
        try:
            self.ser.close()
            self.temp_timer.stop()
            self.sensor_timer.stop()
            
            # Disconnect signals
            self.general_ui.module_name_label.editingFinished.disconnect()
            self.profibus_ui.address_line_edit.editingFinished.disconnect()
            self.general_ui.brightness_combobox.currentIndexChanged.disconnect()
            self.profibus_ui.slot_combobox.currentIndexChanged.disconnect()
            self.general_ui.restore_button.clicked.disconnect()

            # Disconnect signals for comboboxes and others
            for i in range(8):
                self.profibus_ui.channel_comboboxes[i].currentIndexChanged.disconnect()
                self.profibus_ui.units_comboboxes[i].currentIndexChanged.disconnect()
                self.sensor_ui.type_comboboxes[i].currentIndexChanged.disconnect()
                self.sensor_ui.power_comboboxes[i].currentIndexChanged.disconnect()
                self.sensor_ui.name_line_edits[i].editingFinished.disconnect()
                self.curve_ui.name_labels[i].editingFinished.disconnect()
                self.sensor_ui.current_reversal_comboboxes[i].currentIndexChanged.disconnect()
                self.sensor_ui.autorange_comboboxes[i].currentIndexChanged.disconnect()
                self.sensor_ui.range_comboboxes[i].currentIndexChanged.disconnect()
                self.sensor_ui.display_units_comboboxes[i].currentIndexChanged.disconnect()
                self.curve_ui.delete_buttons[i].clicked.disconnect()
                self.curve_ui.curve_comboboxes[i].currentIndexChanged.disconnect()

            self.connection_ui.status_label.setText("<b>Status: </b>        Disconnected")
        except Exception as e:
            print(f"Error: {e}")

    
    def handle_delete_curve(self):
        sender = self.sender()
        i = 1
        for button in self.curve_ui.delete_buttons:
            if (sender == button):
                message = f"CRVDEL {i}\n"
                self.ser.write(message.encode())
                break
            i+=1
        self.curve_ui.curve_comboboxes[i-1].setCurrentIndex(-1)
        

    def handle_curve_change(self):
        try:
            sender = self.sender()
            input = 0
            i = 1
            for combobox in self.curve_ui.curve_comboboxes:
                if combobox == sender:
                    input = i
                    break
                i +=1
            sensor_type_box = self.sensor_ui.layout.itemAtPosition(input, 2).widget()
            sensor_current_box = self.sensor_ui.layout.itemAtPosition(input, 3).widget()
            sensor_autorange_box = self.sensor_ui.layout.itemAtPosition(input, 4).widget()
            sensor_range_box = self.sensor_ui.layout.itemAtPosition(input, 5).widget()
            sensor_unit_box = self.sensor_ui.layout.itemAtPosition(input, 6).widget()
            file = ""
            name = ""
            serial = ""
            format = 0
            coefficient = 0
            index = sender.currentIndex()
            match index:
                case 0:
                    file = "curves/LSCI_DT600.txt"
                    name = "LSCI_DT-600"
                    serial = "Standard C"
                    format = 2
                    limit = 500
                    coefficient = 1
                case 1:
                    file = "curves/LSCI_DT400.txt"
                    name = "LSCI_DT-400"
                    serial = "Standard C"
                    format = 2
                    limit = 475
                    coefficient = 1
                case 2:
                    file = "curves/LSCI_PT100.txt"
                    name = "LSCI_PT-100"
                    serial = "STANDARD"
                    format = 3
                    limit = 800
                    coefficient = 2
                case 3:
                    file = "curves/IEC_PT100_RTD.txt"
                    name = "IEC_PT100_RTD"
                    serial = "STANDARD"
                    format = 3
                    limit = 800
                    coefficient = 2                
                case 4:
                    file = "curves/IEC_PT1000_RTD.txt"
                    name = "IEC_PT1000_RTD"
                    serial = "STANDARD"
                    format = 3
                    limit = 800
                    coefficient = 2
                case 5:
                    file = "curves/SIMULATED_SENSO.txt"
                    name = "Simulated Senso"
                    serial = "Standard C"
                    format = 4
                    limit = 450
                    coefficient = 1                    
            if file != "":
                message = f"CRVDEL {input}\n"
                self.ser.write(message.encode())
                message = f"CRVHDR {input},{name},{serial},{format},{limit},{coefficient}\n"
                self.ser.write(message.encode())
                with open(file, "r") as opened_file:
                    current_index = 0
                    for line in opened_file:
                        current_index+=1
                        values = line.strip().split(',')
                        unit, temp = map(float, values)
                        message = f"CRVPT {input},{current_index},{unit},{temp}\n"
                        self.ser.write(message.encode())

                # Change sensors
                match index:
                    case 0:
                        sensor_type_box.setCurrentIndex(0)
                        sensor_unit_box.setCurrentIndex(0)

                    case 1:
                        sensor_type_box.setCurrentIndex(0)
                        sensor_unit_box.setCurrentIndex(0)

                    case 2:
                        sensor_type_box.setCurrentIndex(1)
                        sensor_current_box.setCurrentIndex(1)
                        sensor_unit_box.setCurrentIndex(0)

                    case 3:
                        sensor_type_box.setCurrentIndex(2)
                        sensor_current_box.setCurrentIndex(0)
                        sensor_autorange_box.setCurrentIndex(0)
                        sensor_range_box.setCurrentIndex(2)
                        sensor_unit_box.setCurrentIndex(2)     
                    case 4:
                        sensor_type_box.setCurrentIndex(2)
                        sensor_current_box.setCurrentIndex(0)
                        sensor_autorange_box.setCurrentIndex(0)
                        sensor_range_box.setCurrentIndex(0)
                        sensor_unit_box.setCurrentIndex(2)    
                    case 5:
                        sensor_type_box.setCurrentIndex(2)
                        sensor_current_box.setCurrentIndex(1)
                        sensor_autorange_box.setCurrentIndex(1)
                        sensor_range_box.setCurrentIndex(3)
                        sensor_unit_box.setCurrentIndex(0)
            
        except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
