from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem
from PySide6.QtCore import QTimer
import serial
import serial.tools.list_ports
from ui.left_ui import LeftUI
from ui.temperature_ui import TemperatureUI
from serialcom.general import read_general_information, read_brightness
from serialcom.profibus import read_address, read_slot_count, read_slots
from serialcom.sensor import read_input_names, read_sensor_setup

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
        self.temp_timer.timeout.connect(self.read_temperature)
        self.sensor_timer = QTimer(self)
        self.sensor_timer.setInterval(10000)  # Update every 10 seconds
        self.sensor_timer.timeout.connect(self.read_sensor_units)

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
        self.read_curves()
        self.read_sensor_units()
        self.read_temperature()

        # Connect signals
        self.general_ui.module_name_label.editingFinished.connect(self.handle_module_name_change)
        self.profibus_ui.address_line_edit.editingFinished.connect(self.handle_address_change)
        self.general_ui.brightness_combobox.currentIndexChanged.connect(self.handle_brightness_change)
        self.profibus_ui.slot_combobox.currentIndexChanged.connect(self.handle_slot_count_change)
        self.general_ui.restore_button.clicked.connect(self.handle_restore_factory_settings)
        # Connect signals for comboboxes and others
        for i in range(8):
            self.profibus_ui.channel_comboboxes[i].currentIndexChanged.connect(self.handle_channel_unit_change)
            self.profibus_ui.units_comboboxes[i].currentIndexChanged.connect(self.handle_channel_unit_change)
            self.sensor_ui.type_comboboxes[i].currentIndexChanged.connect(self.handle_type_change)
            self.sensor_ui.power_comboboxes[i].currentIndexChanged.connect(self.handle_power_change)
            self.sensor_ui.name_line_edits[i].editingFinished.connect(self.handle_name_change)
            self.curve_ui.name_labels[i].editingFinished.connect(self.handle_name_change)
            self.sensor_ui.current_reversal_comboboxes[i].currentIndexChanged.connect(self.handle_sensor_change)
            self.sensor_ui.autorange_comboboxes[i].currentIndexChanged.connect(self.handle_sensor_change)
            self.sensor_ui.range_comboboxes[i].currentIndexChanged.connect(self.handle_sensor_change)
            self.sensor_ui.display_units_comboboxes[i].currentIndexChanged.connect(self.handle_sensor_change)
            self.curve_ui.delete_buttons[i].clicked.connect(self.handle_delete_curve)
            self.curve_ui.curve_comboboxes[i].currentIndexChanged.connect(self.handle_curve_change)

        self.temp_timer.start()
        self.sensor_timer.start()

        self.connection_ui.status_label.setText("<b>Status: </b>        Connected")
    
    def handle_disconnect(self):
        try:
            self.ser.close()
            self.temp_timer.stop()
            self.sensor_timer.stop()
            
            # Disconnect signals
            self.general_ui.module_name_label.editingFinished.disconnect(self.handle_module_name_change)
            self.profibus_ui.address_line_edit.editingFinished.disconnect(self.handle_address_change)
            self.general_ui.brightness_combobox.currentIndexChanged.disconnect(self.handle_brightness_change)
            self.profibus_ui.slot_combobox.currentIndexChanged.disconnect(self.handle_slot_count_change)
            self.general_ui.restore_button.clicked.disconnect(self.handle_restore_factory_settings)

            # Disconnect signals for comboboxes and others
            for i in range(8):
                self.profibus_ui.channel_comboboxes[i].currentIndexChanged.disconnect(self.handle_channel_unit_change)
                self.profibus_ui.units_comboboxes[i].currentIndexChanged.disconnect(self.handle_channel_unit_change)
                self.sensor_ui.type_comboboxes[i].currentIndexChanged.disconnect(self.handle_type_change)
                self.sensor_ui.power_comboboxes[i].currentIndexChanged.disconnect(self.handle_power_change)
                self.sensor_ui.name_line_edits[i].editingFinished.disconnect(self.handle_name_change)
                self.curve_ui.name_labels[i].editingFinished.disconnect(self.handle_name_change)
                self.sensor_ui.current_reversal_comboboxes[i].currentIndexChanged.disconnect(self.handle_sensor_change)
                self.sensor_ui.autorange_comboboxes[i].currentIndexChanged.disconnect(self.handle_sensor_change)
                self.sensor_ui.range_comboboxes[i].currentIndexChanged.disconnect(self.handle_sensor_change)
                self.sensor_ui.display_units_comboboxes[i].currentIndexChanged.disconnect(self.handle_sensor_change)
                self.curve_ui.delete_buttons[i].clicked.disconnect(self.handle_delete_curve)
                self.curve_ui.curve_comboboxes[i].currentIndexChanged.disconnect(self.handle_curve_change)

            self.connection_ui.status_label.setText("<b>Status: </b>        Disconnected")
        except Exception as e:
            print(f"Error: {e}")

    def read_temperature(self):
        try:
            # Write data to the port to ask temperature in Kelvin
            message = "KRDG? 0\n"
            self.ser.write(message.encode())

            # Read temperature data from the port
            data = self.ser.read(1024).decode().strip()
            temperatures = data.split(",")[:8]

            # Update table with formatted temperatures
            for row, temp in enumerate(temperatures):
                if(self.sensor_ui.power_comboboxes[row].currentIndex() == 1):  #if power is on
                    formatted_temp = temp.lstrip('+')  # Remove leading '+'
                    if  '.' in formatted_temp:
                        formatted_temp = formatted_temp.lstrip('0')  # Remove leading '0's
                    if len(formatted_temp) > 0 and formatted_temp[0] == ".":
                        formatted_temp = '0' + formatted_temp
                    formatted_temp = formatted_temp + " K"
                    if formatted_temp == '0.00000 K':
                        message = f"RDGST? {row+1}\n"
                        self.ser.write(message.encode())
                        response = self.ser.read(1024).decode().strip()
                        match response:
                            case "1":
                                formatted_temp = "INV.READ"
                            case "16":
                                formatted_temp = "T.UNDER"
                            case "32":
                                formatted_temp = "T.OVER"
                            case "64":
                                formatted_temp = "S.UNDER"
                            case "128":
                                formatted_temp = "S.OVER"
                    self.temperature_ui.table.setItem(row, 1, QTableWidgetItem(formatted_temp if formatted_temp != '0.00000 K' else '0 K'))
                else:
                    self.temperature_ui.table.setItem(row, 1, QTableWidgetItem(""))

        except Exception as e:
            print(f"Error: {e}")

    def read_sensor_units(self):
        try:
            # Write query to the port to ask sensor units
            message = "SRDG? 0\n"
            self.ser.write(message.encode())

            # Read sensor units data from the port
            data = self.ser.read(1024).decode().strip()
            sensor_units = data.split(",")[:8]

            # Update table with sensor units
            for row, unit in enumerate(sensor_units):
                if(self.sensor_ui.power_comboboxes[row].currentIndex() == 1): # If power is on
                    unit = unit.lstrip('+')  # Remove leading '+'
                    if '.' in unit:
                        unit = unit.lstrip('0')  # Remove leading '0's
                    if len(unit) > 0 and unit[0] == ".":
                        unit = '0' + unit
                    if(self.sensor_ui.type_comboboxes[row].currentIndex() == 0):
                        unit = unit + " V"
                    else:
                        unit = unit + " Ω"
                    self.temperature_ui.table.setItem(row, 2, QTableWidgetItem(unit if (unit != '0.000 V' and unit != '0.000 Ω') else '0'))
                    self.set_excitation(row)
                    self.calculate_power(row)
                else:
                    self.temperature_ui.table.setItem(row, 2, QTableWidgetItem(""))
                    self.temperature_ui.table.setItem(row, 3, QTableWidgetItem(""))
                    self.temperature_ui.table.setItem(row, 4, QTableWidgetItem(""))

        except Exception as e:
            print(f"Error: {e}")

    def read_curves(self):
        try:
            for row in range(8):
                input_number = row + 1
                message = f"CRVHDR? {input_number}\n"
                self.ser.write(message.encode())
                response = self.ser.read(1024).decode().strip().split(",")[:5]
                name = response[0].strip()
                if (name == "LSCI_DT-600"):
                    self.curve_ui.curve_comboboxes[row].setCurrentIndex(0)
                elif (name == "LSCI_DT-400"):
                    self.curve_ui.curve_comboboxes[row].setCurrentIndex(1)
                elif (name == "LSCI_PT-100"):
                    self.curve_ui.curve_comboboxes[row].setCurrentIndex(2)
                elif (name == "IEC_PT100_RTD"):
                    self.curve_ui.curve_comboboxes[row].setCurrentIndex(3)
                elif (name == "IEC_PT1000_RTD"):
                    self.curve_ui.curve_comboboxes[row].setCurrentIndex(4)
                elif (name == "Simulated Senso"):
                    self.curve_ui.curve_comboboxes[row].setCurrentIndex(5)
                else:
                    self.curve_ui.curve_comboboxes[row].setCurrentIndex(-1)
        except Exception as e:
            print(f"Error: {e}")

    def calculate_power(self, row):
        try:
            sensor_text = self.temperature_ui.table.item(row, 2).text()
            excitation_text =self.temperature_ui.table.item(row, 3).text()

            if (len(sensor_text) == 0 or len(excitation_text) == 0):
                return
            power_value = 0
            sensor_unit = sensor_text[-1]
            excitation_unit = excitation_text[-2:]

            sensor_value = float(sensor_text[:-2])
            excitation_value = float(excitation_text[:-3])

            match excitation_unit:
                case "mA":
                    excitation_value = excitation_value /1000
                case "µA":
                    excitation_value = excitation_value /1000000
                case "nA":
                    excitation_value = excitation_value /1000000000

            match sensor_unit:
                case "V":
                    power_value = excitation_value * sensor_value
                case "Ω":
                    power_value = excitation_value * excitation_value * sensor_value

            power_unit = " W"
            multiplier = 1
            if power_value < 1:
                # Determine the appropriate multiplier based on the power_value
                if power_value < 0.000001:
                    multiplier = 1000000000
                    power_unit = " nW"
                elif power_value < 0.001:
                    multiplier = 1000000
                    power_unit = " µW"
                else:
                    multiplier = 1000
                    power_unit = " mW"

            # Multiply the number by the appropriate multiplier
            adjusted_num = power_value * multiplier
            power = str(round(adjusted_num, 2)) + power_unit
            self.temperature_ui.table.item(row, 4).setText(power)

        except Exception as e:
            print(f"Error: {e}")
    
    def set_excitation(self, row):
        range_combo_box = self.sensor_ui.layout.itemAtPosition(row+1, 5).widget()
        excitation = range_combo_box.currentText()
        # Extracting the part between parentheses
        start_index = excitation.find('(') + 1
        end_index = excitation.find(')', start_index)
        parsed_excitation = excitation[start_index:end_index]
        self.temperature_ui.table.setItem(row, 3, QTableWidgetItem(parsed_excitation))


    def handle_module_name_change(self):
        new_name = self.general_ui.module_name_label.text()
        message = f"MODNAME {new_name}\n"
        self.ser.write(message.encode())

    def handle_address_change(self):
        new_address = int(self.profibus_ui.address_line_edit.text())
        message = f"ADDR {new_address}\n"
        self.ser.write(message.encode())

    def handle_brightness_change(self):
        selected_brightness = self.general_ui.brightness_combobox.currentIndex()
        message = f"BRIGT {selected_brightness}\n"
        self.ser.write(message.encode())
    
    def handle_slot_count_change(self):
        selected_slot = self.profibus_ui.slot_combobox.currentIndex()
        message = f"PROFINUM {selected_slot}\n"
        self.ser.write(message.encode())
    
    def handle_channel_unit_change(self):
        sender_combobox = self.sender()
        row = self.profibus_ui.layout.getItemPosition(self.profibus_ui.layout.indexOf(sender_combobox))[0]
        input_number = row - 3  # Offset by 3 to account for the header rows

        channel_index = self.profibus_ui.channel_comboboxes[input_number-1].currentIndex()
        unit_index = self.profibus_ui.units_comboboxes[input_number-1].currentIndex()

        self.handle_comboboxes_change(input_number, channel_index, unit_index)

    def handle_comboboxes_change(self, input_number, channel_index, unit_index):
        message = f"PROFISLOT {input_number},{channel_index+1},{unit_index+1}\n"
        self.ser.write(message.encode())
    
    def handle_name_change(self):
        sender = self.sender()
        new_name = sender.text()
        row = 0
        i =0
        found = False
        for line_edit in self.sensor_ui.name_line_edits:
            if (line_edit == sender):
                row = i
                found = True
                break
            i+=1
        
        if (not found):
            j =0
            for label in self.curve_ui.name_labels:
                if (label == sender):
                    row = j
                    break
                j+=1

        message = f"INNAME {row+1},{new_name}\n"
        self.ser.write(message.encode())

        self.temperature_ui.table.setItem(row, 0, QTableWidgetItem(new_name))
        self.sensor_ui.name_line_edits[row].setText(new_name)
        self.curve_ui.name_labels[row].setText(new_name)
    
    def handle_restore_factory_settings(self):
        message = f"DFLT 99\n"
        self.ser.write(message.encode())
    
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

    def handle_sensor_change(self):
        #TODO: if type/power changes this function also gets called for every combobox -> fix that
        
        # Get the index of the combo box that triggered the change
        sender_combo_box = self.sender()

        # Get the row number of the combo box in the layout
        row = self.sensor_ui.layout.getItemPosition(self.sensor_ui.layout.indexOf(sender_combo_box))[0]

        # Get the values
        power = self.sensor_ui.layout.itemAtPosition(row, 0).widget().currentIndex()
        type = self.sensor_ui.layout.itemAtPosition(row, 2).widget().currentIndex() +1
        current_reversal = self.sensor_ui.layout.itemAtPosition(row, 3).widget().currentIndex()
        autorange = self.sensor_ui.layout.itemAtPosition(row, 4).widget().currentIndex()
        selected_range = self.sensor_ui.layout.itemAtPosition(row, 5).widget().currentIndex()
        unit = self.sensor_ui.layout.itemAtPosition(row, 6).widget().currentIndex() +1

        message = f"INTYPE {row},{type},{autorange},{selected_range},{current_reversal},{unit},{power}\n"
        self.ser.write(message.encode())

    def handle_type_change(self):
        # Get the index of the combo box that triggered the change
        sender_combo_box = self.sender()

        # Get the row number of the combo box in the layout
        row = self.sensor_ui.layout.getItemPosition(self.sensor_ui.layout.indexOf(sender_combo_box))[0]

        # Get the selected type
        selected_type = sender_combo_box.currentText()

        # Get the relevant combo boxes for the current row
        current_reversal_combo_box = self.sensor_ui.layout.itemAtPosition(row, 3).widget()
        autorange_combo_box = self.sensor_ui.layout.itemAtPosition(row, 4).widget()
        range_combo_box = self.sensor_ui.layout.itemAtPosition(row, 5).widget()
        units_combo_box = self.sensor_ui.layout.itemAtPosition(row, 6).widget()
        units_combo_box.setEnabled(True)
        units_combo_box.setStyleSheet("")

        # Apply constraints based on the selected type
        if selected_type == "Diode":
            current_reversal_combo_box.setCurrentIndex(0)
            current_reversal_combo_box.setEnabled(False)  # Disable current reversal
            current_reversal_combo_box.setStyleSheet("QComboBox { color: darkgray; }")
            autorange_combo_box.setCurrentIndex(0)  # Set autorange to "Off"
            autorange_combo_box.setEnabled(False)  # Disable autorange
            autorange_combo_box.setStyleSheet("QComboBox { color: darkgray; }")
            range_combo_box.clear()
            range_combo_box.addItems(["7.5 V (10 µA)"])
            range_combo_box.setEnabled(False)  # Disable range
            range_combo_box.setStyleSheet("QComboBox { color: darkgray; }")
        elif selected_type == "Platinum RTD":
            autorange_combo_box.setCurrentIndex(0)  # Set autorange to "Off"
            autorange_combo_box.setEnabled(False)  # Disable autorange
            autorange_combo_box.setStyleSheet("QComboBox { color: darkgray; }")
            range_combo_box.clear()
            range_combo_box.addItems(["1 kΩ (1 mA)"])
            range_combo_box.setEnabled(False)  # Disable range
            range_combo_box.setStyleSheet("QComboBox { color: darkgray; }")
            current_reversal_combo_box.setEnabled(True)  # Enable current reversal
            current_reversal_combo_box.setStyleSheet("")
        else:
            current_reversal_combo_box.setEnabled(True)
            current_reversal_combo_box.setStyleSheet("")
            autorange_combo_box.setEnabled(True)
            autorange_combo_box.setStyleSheet("")
            range_combo_box.setEnabled(True)
            range_combo_box.setStyleSheet("")
            range_combo_box.clear()
            range_combo_box.addItems(["10 Ω (1 mA)", "30 Ω (300 µA)", "100 Ω (100 µA)",
                                    "300 Ω (30 µA)", "1 kΩ (10 µA)", "3 kΩ (3 µA)", "10 kΩ (1 µA)",
                                    "30 kΩ (300 nA)", "100 kΩ (100 nA)"])
        
        # Get the values
        power = self.sensor_ui.layout.itemAtPosition(row, 0).widget().currentIndex()
        type = self.sensor_ui.layout.itemAtPosition(row, 2).widget().currentIndex() +1
        current_reversal = self.sensor_ui.layout.itemAtPosition(row, 3).widget().currentIndex()
        autorange = self.sensor_ui.layout.itemAtPosition(row, 4).widget().currentIndex()
        selected_range = self.sensor_ui.layout.itemAtPosition(row, 5).widget().currentIndex()
        unit = self.sensor_ui.layout.itemAtPosition(row, 6).widget().currentIndex() +1

        message = f"INTYPE {row},{type},{autorange},{selected_range},{current_reversal},{unit},{power}\n"
        self.ser.write(message.encode())
            
    def handle_power_change(self):
        # Get the index of the combo box that triggered the change
        sender_combo_box = self.sender()

        # Get the row number of the combo box in the layout
        row = self.sensor_ui.layout.getItemPosition(self.sensor_ui.layout.indexOf(sender_combo_box))[0]
        
        # Get the selected power state
        selected_power_state = sender_combo_box.currentText()

        # Get the values
        power = self.sensor_ui.layout.itemAtPosition(row, 0).widget().currentIndex()
        type = self.sensor_ui.layout.itemAtPosition(row, 2).widget().currentIndex() +1
        current_reversal = self.sensor_ui.layout.itemAtPosition(row, 3).widget().currentIndex()
        autorange = self.sensor_ui.layout.itemAtPosition(row, 4).widget().currentIndex()
        selected_range = self.sensor_ui.layout.itemAtPosition(row, 5).widget().currentIndex()
        unit = self.sensor_ui.layout.itemAtPosition(row, 6).widget().currentIndex() +1

        #range combobox
        range_combo_box = self.sensor_ui.layout.itemAtPosition(row, 5).widget()


        message = f"INTYPE {row},{type},{autorange},{selected_range},{current_reversal},{unit},{power}\n"
        self.ser.write(message.encode())

        if selected_power_state == "On":
            # Diode
            if type == 1:
                for col in range(2, 7):
                    widget = self.sensor_ui.layout.itemAtPosition(row, col).widget()
                    if col in [2, 6]:  # Type and Display Units columns
                        widget.setEnabled(True)
                        widget.setStyleSheet("")
            # Platinum RTD
            elif type == 2:
                for col in range(2, 7):
                    widget = self.sensor_ui.layout.itemAtPosition(row, col).widget()
                    if col in [2, 3, 6]:  # Type, Current Reversal, and Display Units columns
                        widget.setEnabled(True)
                        widget.setStyleSheet("")
            # NTC RTD
            elif type == 3:
                range_combo_box.clear()
                range_combo_box.addItems(["10 Ω (1 mA)", "30 Ω (300 µA)", "100 Ω (100 µA)",
                "300 Ω (30 µA)", "1 kΩ (10 µA)", "3 kΩ (3 µA)", "10 kΩ (1 µA)",
                "30 kΩ (300 nA)", "100 kΩ (100 nA)"])
                range_combo_box.setCurrentIndex(int(selected_range))
                for col in range(2, 7):
                    widget = self.sensor_ui.layout.itemAtPosition(row, col).widget()
                    widget.setEnabled(True)
                    widget.setStyleSheet("")

            else:
                # Only enable type column
                widget = self.sensor_ui.layout.itemAtPosition(row, 2).widget()
                widget.setEnabled(True)
                widget.setStyleSheet("")
        else:
            for col in range(2, 7):
                widget = self.sensor_ui.layout.itemAtPosition(row, col).widget()
                widget.setEnabled(False)
                widget.setStyleSheet("QComboBox { color: darkgray; }")


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
