from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QSizePolicy, QLabel, QGridLayout, QLineEdit, QFrame, QComboBox, QPushButton, QHeaderView, QLayout
from PySide6.QtCore import QTimer
import serial
import time

class TemperatureWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)

        # Left layout for general information
        self.left_layout = QVBoxLayout()

        # General section frame
        self.general_section_frame = QFrame()
        self.general_section_frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.general_section_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # General section grid layout
        self.general_section_layout = QGridLayout(self.general_section_frame)

        # General label 
        self.general_label = QLabel("<b>General</b>")
        self.general_label.setStyleSheet("font-size: 14pt;")

        # Restore factory settings button
        self.restore_button = QPushButton("Restore factory settings")

        # Labels for general information
        self.module_name_label = QLineEdit()
        self.serial_number_label = QLabel()
        self.firmware_version_label = QLabel()
        self.brightness_combobox = QComboBox()
        self.brightness_combobox.addItems(["Off", "Low", "Medium", "High", "Max"])

        # Add labels to general grid layout
        self.general_section_layout.addWidget(QLabel("<b>Name</b>"), 0, 0)
        self.general_section_layout.addWidget(self.module_name_label, 0, 1)
        self.general_section_layout.addWidget(QLabel("<b>Serial Number</b>"), 1, 0)
        self.general_section_layout.addWidget(self.serial_number_label, 1, 1)
        self.general_section_layout.addWidget(QLabel("<b>Firmware Version</b>"), 2, 0)
        self.general_section_layout.addWidget(self.firmware_version_label, 2, 1)
        self.general_section_layout.addWidget(QLabel("<b>Screen Brightness</b>"), 3, 0)
        self.general_section_layout.addWidget(self.brightness_combobox, 3, 1)
        self.general_section_layout.addWidget(self.restore_button, 4, 0, 1, 2)

        # Create QHBoxlayout for Profibus and Curve part
        self.left_hlayout = QHBoxLayout()

        # Set size constraint to allow stretching
        self.left_hlayout.setSizeConstraint(QLayout.SetMinimumSize)

        # Profibus communication section
        # Vbox for Profibus part
        self.profibus_vlayout = QVBoxLayout()

        # New QLabel for PROFIBUS
        self.profibus_label = QLabel("<b>PROFIBUS communication</b>")
        self.profibus_label.setStyleSheet("font-size: 14pt;")

        # New QFrame for PROFIBUS communication
        self.profibus_frame = QFrame()
        self.profibus_frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.profibus_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Grid layout for PROFIBUS communication
        self.profibus_layout = QGridLayout()
        self.profibus_frame.setLayout(self.profibus_layout)
        self.profibus_layout.addWidget(QLabel("<b>Address</b>"), 0, 0)
        self.address_line_edit = QLineEdit()
        self.profibus_layout.addWidget(self.address_line_edit, 0, 1)
        self.profibus_layout.addWidget(QLabel("<b>Slot Count</b>"), 1, 0)
        self.slot_count_combobox = QComboBox()
        self.slot_count_combobox.addItems([str(i) for i in range(1, 9)])
        self.profibus_layout.addWidget(self.slot_count_combobox, 1, 1)

        # Add an empty row
        self.profibus_layout.addWidget(QLabel(""), 2, 0)

        # Header labels
        self.profibus_layout.addWidget(QLabel("<b>Channel</b>"), 3, 1)
        self.profibus_layout.addWidget(QLabel("<b>Units</b>"), 3, 2)

        # Labels for Slot1-8
        for i in range(1, 9):
            self.profibus_layout.addWidget(QLabel(f"<b>Slot {i}</b>"), i + 3, 0)

        # Comboboxes for Channel
        self.channel_comboboxes = []
        for i in range(1, 9):
            channel_combobox = QComboBox()
            channel_combobox.addItems([str(j) for j in range(1, 9)])
            self.channel_comboboxes.append(channel_combobox)
            self.profibus_layout.addWidget(channel_combobox, i + 3, 1)

        # Comboboxes for Units
        self.units_comboboxes = []
        for i in range(1, 9):
            units_combobox = QComboBox()
            units_combobox.addItems(["Kelvin", "Celsius", "sensor", "Fahrenheit"])
            self.units_comboboxes.append(units_combobox)
            self.profibus_layout.addWidget(units_combobox, i + 3, 2)
        
        # Add widgets to vlayout
        self.profibus_vlayout.addWidget(self.profibus_label)
        self.profibus_vlayout.addWidget(self.profibus_frame)

        # Curve setup section 
        # Vbox for Curve part
        self.curve_vlayout = QVBoxLayout()

        # Label for curve setup
        self.curve_label = QLabel("<b>Curve setup</b>")
        self.curve_label.setStyleSheet("font-size: 14pt;")

        # New QFrame for curve section
        self.curve_frame = QFrame()
        self.curve_frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.curve_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Grid layout for curve section
        self.curve_layout = QGridLayout()
        self.curve_frame.setLayout(self.curve_layout)

        # Add labels for curve section
        self.curve_layout.addWidget(QLabel("<b>Name</b>"), 0, 0)
        self.curve_layout.addWidget(QLabel("<b>Curve</b>"), 0, 1)

        # Add QLine_edit for Name
        self.curve_name_labels = []
        for row in range(1, 9):
            label = QLineEdit("")
            self.curve_layout.addWidget(label, row, 0)
            self.curve_name_labels.append(label)

        # Add rows for curve section
        self.curve_comboboxes = []
        for i in range(1, 9):
            combobox = QComboBox()
            combobox.addItems(["LSCI DT-600", "LSCI DT-400", "LSCI PT-100", "IEC PT100 RTD", "IEC PT1000 RTD", "Simulated Sensor-NTC"])
            self.curve_comboboxes.append(combobox)
            self.curve_layout.addWidget(combobox, i, 1)
        
        # Delete buttons for curves
        self.curve_delete_buttons = []
        for i in range(1, 9):
            button = QPushButton("DEL")
            self.curve_delete_buttons.append(button)
            self.curve_layout.addWidget(button, i, 2)

        
        # Add widgets to vlayout
        self.curve_vlayout.addWidget(self.curve_label)
        self.curve_vlayout.addWidget(self.curve_frame)

        # Add profibus and curve layouts to left_hlayout
        self.left_hlayout.addLayout(self.profibus_vlayout, stretch=1)
        self.left_hlayout.addLayout(self.curve_vlayout, stretch=1)

        # Sensor setup section
        self.sensor_label = QLabel("<b>Sensor setup</b>")
        self.sensor_label.setStyleSheet("font-size: 14pt;")

        # New QFrame for sensor section
        self.sensor_frame = QFrame()
        self.sensor_frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.sensor_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Grid layout for sensor section
        self.sensor_layout = QGridLayout()
        self.sensor_frame.setLayout(self.sensor_layout)

        # Labels for sensor section
        sensor_labels = ["Power", "Name", "Type", "Current Reversal", "Autorange", "Range", "Display Units"]

        # Add labels to sensor grid layout
        for col, label in enumerate(sensor_labels):
            self.sensor_layout.addWidget(QLabel(f"<b>{label}</b>"), 0, col)

        # Add QComboBox for Power (On/Off)
        power_options = ["Off", "On"]
        self.power_comboboxes = []
        for row in range(1, 9):
            combo_box = QComboBox()
            combo_box.addItems(power_options)
            self.sensor_layout.addWidget(combo_box, row, 0)
            self.power_comboboxes.append(combo_box)

        # Add QLineEdit for Name
        self.line_edits = []
        for row in range(1, 9):
            line_edit = QLineEdit()
            self.sensor_layout.addWidget(line_edit, row, 1)
            self.line_edits.append(line_edit)

        # Add QComboBox for Type
        sensor_types = ["Diode", "Platinum RTD", "NTC RTD"]
        self.type_comboboxes = []  # Store the combo boxes in a list to access them later if needed
        for row in range(1, 9):
            combo_box = QComboBox()
            combo_box.addItems(sensor_types)
            self.sensor_layout.addWidget(combo_box, row, 2)
            self.type_comboboxes.append(combo_box)

        # Add QComboBox for Current Reversal
        on_off_values = ["Off", "On"]
        self.current_reversal_comboboxes = []
        for row in range(1, 9):
                combo_box = QComboBox()
                combo_box.addItems(on_off_values)
                self.current_reversal_comboboxes.append(combo_box)
                self.sensor_layout.addWidget(combo_box, row, 3)

        # Add QComboBox for Autorange
        on_off_values = ["Off", "On"]
        self.autorange_comboboxes = []
        for row in range(1, 9):
                combo_box = QComboBox()
                combo_box.addItems(on_off_values)
                self.autorange_comboboxes.append(combo_box)
                self.sensor_layout.addWidget(combo_box, row, 4)

        # Add comboboxes for Range
        range_values = ["7.5 V (10 µA)", "1 kΩ (1 mA)", "10 Ω (1 mA)", "30 Ω (300 µA)", "100 Ω (100 µA)", "300 Ω (30 µA)",
                        "1 kΩ (10 µA)", "3 kΩ (3 µA)", "10 kΩ (1 µA)", "30 kΩ (300 nA)", "100 kΩ (100 nA)"]
        self.range_comboboxes = []
        for row in range(1, 9):
            combo_box = QComboBox()
            combo_box.addItems(range_values)
            self.range_comboboxes.append(combo_box)
            self.sensor_layout.addWidget(combo_box, row, 5)
            
        # Add comboboxes for Display Units
        display_units = ["Kelvin", "Celsius", "Sensor", "Fahrenheit"]
        self.display_units_comboboxes = []
        for row in range(1, 9):
            combo_box = QComboBox()
            combo_box.addItems(display_units)
            self.display_units_comboboxes.append(combo_box)
            self.sensor_layout.addWidget(combo_box, row, 6)

        # Add sections to general layout
        self.left_layout.addWidget(self.general_label)
        self.left_layout.addWidget(self.general_section_frame)
        self.left_layout.addLayout(self.left_hlayout)
        self.left_layout.addWidget(self.sensor_label)
        self.left_layout.addWidget(self.sensor_frame)

        # Stretch the left_hlayout within the left_layout
        self.left_layout.setStretch(2, 1)

        # Right layout for temperature table
        self.right_layout = QVBoxLayout()
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setRowCount(8)
        self.table_widget.setHorizontalHeaderLabels(["Name", "Temperature", "Sensor units", "Excitation", "Power"])

        # Populate table with sample data
        for row in range(8):
            self.table_widget.setItem(row, 0, QTableWidgetItem(""))
            self.table_widget.setItem(row, 1, QTableWidgetItem(""))
            self.table_widget.setItem(row, 2, QTableWidgetItem(""))
            self.table_widget.setItem(row, 3, QTableWidgetItem(""))
            self.table_widget.setItem(row, 4, QTableWidgetItem(""))

        # Set size policy to expand vertically
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set vertical header to resize to contents
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Add table to right layout
        self.right_layout.addWidget(self.table_widget)

        # Add left and right layouts to main layout
        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.right_layout)

        # Set serial port settings and read data
        self.port = '/dev/ttyUSB0'
        self.baudrate = 115200
        self.timeout = 1
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        self.read_general_information()
        self.read_brightness()
        self.read_input_names()
        self.read_address()
        self.read_slot_count()
        self.read_slots()
        self.read_sensor_setup()
        self.read_curves()
        self.read_sensor_units()
        self.read_temperature()

        # Start timer for updating temperature
        self.temp_timer = QTimer(self)
        self.temp_timer.setInterval(10000)  # Update every 10 seconds
        self.temp_timer.timeout.connect(self.read_temperature)
        self.temp_timer.start()

        # Start timer for updating sensor units
        self.sensor_timer = QTimer(self)
        self.sensor_timer.setInterval(10000)  # Update every 10 seconds
        self.sensor_timer.timeout.connect(self.read_temperature)
        self.sensor_timer.start()

        # Connect signals
        self.module_name_label.editingFinished.connect(self.handle_module_name_change)
        self.address_line_edit.editingFinished.connect(self.handle_address_change)
        self.brightness_combobox.currentIndexChanged.connect(self.handle_brightness_change)
        self.slot_count_combobox.currentIndexChanged.connect(self.handle_slot_count_change)
        self.restore_button.clicked.connect(self.restore_factory_settings)
        # Connect signals for comboboxes and others
        for i in range(8):
            self.channel_comboboxes[i].currentIndexChanged.connect(self.handle_channel_unit_change)
            self.units_comboboxes[i].currentIndexChanged.connect(self.handle_channel_unit_change)
            self.type_comboboxes[i].currentIndexChanged.connect(self.handle_type_change)
            self.power_comboboxes[i].currentIndexChanged.connect(self.handle_power_change)
            self.line_edits[i].editingFinished.connect(self.handle_name_change)
            self.curve_name_labels[i].editingFinished.connect(self.handle_name_change)
            self.current_reversal_comboboxes[i].currentIndexChanged.connect(self.handle_sensor_change)
            self.autorange_comboboxes[i].currentIndexChanged.connect(self.handle_sensor_change)
            self.range_comboboxes[i].currentIndexChanged.connect(self.handle_sensor_change)
            self.display_units_comboboxes[i].currentIndexChanged.connect(self.handle_sensor_change)
            self.curve_delete_buttons[i].clicked.connect(self.delete_curve)
            self.curve_comboboxes[i].currentIndexChanged.connect(self.handle_curve_change)


    def read_general_information(self):
        try:
            # Retrieve and display module name
            module_message = "MODNAME?\n"
            self.ser.write(module_message.encode())
            module_name = self.ser.read(1024).decode().strip()
            self.module_name_label.setText(module_name)

            # Send command to get general information
            message = "*IDN?\n"
            self.ser.write(message.encode())

            # Read response and split into components
            data = self.ser.read(1024).decode().strip()
            components = data.split(",")

            # Update labels with general information
            self.serial_number_label.setText(components[2])
            self.firmware_version_label.setText(components[3])

        except serial.SerialException as e:
            print(f"Error: {e}")

    def read_brightness(self):
        try:
            # Retrieve and display brightness
            message = "BRIGT?\n"
            self.ser.write(message.encode())
            brightness_value = int(self.ser.read(1024).decode().strip())

            # Set the current index of the combo box based on the brightness value
            self.brightness_combobox.setCurrentIndex(brightness_value)

        except serial.SerialException as e:
            print(f"Error: {e}")

    def read_input_names(self):
        try:
            for row in range(8):
                input_number = row + 1
                message = f"INNAME? {input_number}\n"
                self.ser.write(message.encode())
                name = self.ser.read(1024).decode().strip()
                self.table_widget.setItem(row, 0, QTableWidgetItem(name))
                self.line_edits[row].setText(name)
                self.curve_name_labels[row].setText(name)
        except serial.SerialException as e:
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
                if(self.power_comboboxes[row].currentIndex() == 1):  #if power is on
                    formatted_temp = temp.lstrip('+')  # Remove leading '+'
                    if  '.' in formatted_temp:
                        formatted_temp = formatted_temp.lstrip('0')  # Remove leading '0's
                    if formatted_temp[0] == ".":
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
                    self.table_widget.setItem(row, 1, QTableWidgetItem(formatted_temp if formatted_temp != '0.00000 K' else '0 K'))
                else:
                    self.table_widget.setItem(row, 1, QTableWidgetItem(""))

        except serial.SerialException as e:
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
                if(self.power_comboboxes[row].currentIndex() == 1): # If power is on
                    unit = unit.lstrip('+')  # Remove leading '+'
                    if '.' in unit:
                        unit = unit.lstrip('0')  # Remove leading '0's
                    if unit[0] == ".":
                        unit = '0' + unit
                    self.table_widget.setItem(row, 2, QTableWidgetItem(unit if unit != '0.000' else '0'))
                else:
                    self.table_widget.setItem(row, 2, QTableWidgetItem(""))

        except serial.SerialException as e:
            print(f"Error: {e}")

    def read_curves(self):
        try:
            for row in range(8):
                input_number = row + 1
                message = f"CRVHDR? {input_number}\n"
                self.ser.write(message.encode())
                response = self.ser.read(1024).decode().strip().split(",")[:5]
                name = response[0].strip()
                value = response[2]
                excitation = '10µA' if value == '2' else '1mA' if value == '3' else ''
                # self.table_widget.setItem(row, 3, QTableWidgetItem(excitation))
                if (name == "LSCI_DT-600"):
                    self.curve_comboboxes[row].setCurrentIndex(0)
                elif (name == "LSCI_DT-400"):
                    self.curve_comboboxes[row].setCurrentIndex(1)
                elif (name == "LSCI_PT-100"):
                    self.curve_comboboxes[row].setCurrentIndex(2)
                elif (name == "IEC_PT100_RTD"):
                    self.curve_comboboxes[row].setCurrentIndex(3)
                elif (name == "IEC_PT1000_RTD"):
                    self.curve_comboboxes[row].setCurrentIndex(4)
                elif (name == "Simulated Senso"):
                    self.curve_comboboxes[row].setCurrentIndex(5)
                else:
                    self.curve_comboboxes[row].setCurrentIndex(-1)
        except serial.SerialException as e:
            print(f"Error: {e}")
    
    def read_address(self):
        try:
            message = "ADDR?\n"
            self.ser.write(message.encode())
            address = self.ser.read(1024).decode().strip()
            self.address_line_edit.setText(address)

        except serial.SerialException as e:
            print(f"Error: {e}")

    def read_slot_count(self):
        try:
            message = "PROFINUM?\n"
            self.ser.write(message.encode())
            value = int(self.ser.read(1024).decode().strip())
            self.slot_count_combobox.setCurrentIndex(value)

        except serial.SerialException as e:
            print(f"Error: {e}")
    
    def read_slots(self):
        try:
            for row in range(8):
                input_number = row + 1
                message = f"PROFISLOT? {input_number}\n"
                self.ser.write(message.encode())
                data = self.ser.read(1024).decode().strip().split(",")[:2]
                self.channel_comboboxes[row].setCurrentIndex(int(data[0])-1)
                self.units_comboboxes[row].setCurrentIndex(int(data[1])-1)

        except serial.SerialException as e:
            print(f"Error: {e}")

    def handle_module_name_change(self):
        new_name = self.module_name_label.text()
        message = f"MODNAME {new_name}\n"
        self.ser.write(message.encode())

    def handle_address_change(self):
        new_address = int(self.address_line_edit.text())
        message = f"ADDR {new_address}\n"
        self.ser.write(message.encode())

    def handle_brightness_change(self, index):
        selected_brightness = self.brightness_combobox.currentIndex()
        message = f"BRIGT {selected_brightness}\n"
        self.ser.write(message.encode())
    
    def handle_slot_count_change(self, index):
        selected_slot = self.slot_count_combobox.currentIndex()
        message = f"PROFINUM {selected_slot}\n"
        self.ser.write(message.encode())
    
    def handle_channel_unit_change(self):
        sender_combobox = self.sender()
        row = self.profibus_layout.getItemPosition(self.profibus_layout.indexOf(sender_combobox))[0]
        input_number = row - 3  # Offset by 3 to account for the header rows

        channel_index = self.channel_comboboxes[input_number-1].currentIndex()
        unit_index = self.units_comboboxes[input_number-1].currentIndex()

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
        for line_edit in self.line_edits:
            if (line_edit == sender):
                row = i
                found = True
                break
            i+=1
        
        if (not found):
            j =0
            for label in self.curve_name_labels:
                if (label == sender):
                    row = j
                    break
                j+=1

        message = f"INNAME {row+1},{new_name}\n"
        self.ser.write(message.encode())

        self.table_widget.setItem(row, 0, QTableWidgetItem(new_name))
        self.line_edits[row].setText(new_name)
        self.curve_name_labels[row].setText(new_name)
    
    def restore_factory_settings(self):
        message = f"DFLT 99\n"
        self.ser.write(message.encode())
    
    def delete_curve(self):
        sender = self.sender()
        i = 1
        for button in self.curve_delete_buttons:
            if (sender == button):
                message = f"CRVDEL {i}\n"
                self.ser.write(message.encode())
                break
            i+=1
        self.curve_comboboxes[i-1].setCurrentIndex(-1)

    def handle_sensor_change(self, index):
        #TODO: if type/power changes this function also gets called for every combobox -> fix that
        
        # Get the index of the combo box that triggered the change
        sender_combo_box = self.sender()

        # Get the row number of the combo box in the layout
        row = self.sensor_layout.getItemPosition(self.sensor_layout.indexOf(sender_combo_box))[0]

        # Get the values
        power = self.sensor_layout.itemAtPosition(row, 0).widget().currentIndex()
        type = self.sensor_layout.itemAtPosition(row, 2).widget().currentIndex() +1
        current_reversal = self.sensor_layout.itemAtPosition(row, 3).widget().currentIndex()
        autorange = self.sensor_layout.itemAtPosition(row, 4).widget().currentIndex()
        selected_range = self.sensor_layout.itemAtPosition(row, 5).widget().currentIndex()
        unit = self.sensor_layout.itemAtPosition(row, 6).widget().currentIndex() +1

        message = f"INTYPE {row},{type},{autorange},{selected_range},{current_reversal},{unit},{power}\n"
        self.ser.write(message.encode())

    def handle_type_change(self, index):
        # Get the index of the combo box that triggered the change
        sender_combo_box = self.sender()

        # Get the row number of the combo box in the layout
        row = self.sensor_layout.getItemPosition(self.sensor_layout.indexOf(sender_combo_box))[0]

        # Get the selected type
        selected_type = sender_combo_box.currentText()

        # Get the relevant combo boxes for the current row
        current_reversal_combo_box = self.sensor_layout.itemAtPosition(row, 3).widget()
        autorange_combo_box = self.sensor_layout.itemAtPosition(row, 4).widget()
        range_combo_box = self.sensor_layout.itemAtPosition(row, 5).widget()
        units_combo_box = self.sensor_layout.itemAtPosition(row, 6).widget()
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
        power = self.sensor_layout.itemAtPosition(row, 0).widget().currentIndex()
        type = self.sensor_layout.itemAtPosition(row, 2).widget().currentIndex() +1
        current_reversal = self.sensor_layout.itemAtPosition(row, 3).widget().currentIndex()
        autorange = self.sensor_layout.itemAtPosition(row, 4).widget().currentIndex()
        selected_range = self.sensor_layout.itemAtPosition(row, 5).widget().currentIndex()
        unit = self.sensor_layout.itemAtPosition(row, 6).widget().currentIndex() +1

        message = f"INTYPE {row},{type},{autorange},{selected_range},{current_reversal},{unit},{power}\n"
        self.ser.write(message.encode())
            
    def handle_power_change(self, index):
        # Get the index of the combo box that triggered the change
        sender_combo_box = self.sender()

        # Get the row number of the combo box in the layout
        row = self.sensor_layout.getItemPosition(self.sensor_layout.indexOf(sender_combo_box))[0]
        
        # Get the selected power state
        selected_power_state = sender_combo_box.currentText()

        # Get the values
        power = self.sensor_layout.itemAtPosition(row, 0).widget().currentIndex()
        type = self.sensor_layout.itemAtPosition(row, 2).widget().currentIndex() +1
        current_reversal = self.sensor_layout.itemAtPosition(row, 3).widget().currentIndex()
        autorange = self.sensor_layout.itemAtPosition(row, 4).widget().currentIndex()
        selected_range = self.sensor_layout.itemAtPosition(row, 5).widget().currentIndex()
        unit = self.sensor_layout.itemAtPosition(row, 6).widget().currentIndex() +1

        #range combobox
        range_combo_box = self.sensor_layout.itemAtPosition(row, 5).widget()


        message = f"INTYPE {row},{type},{autorange},{selected_range},{current_reversal},{unit},{power}\n"
        self.ser.write(message.encode())

        if selected_power_state == "On":
            # Diode
            if type == 1:
                for col in range(2, 7):
                    widget = self.sensor_layout.itemAtPosition(row, col).widget()
                    if col in [2, 6]:  # Type and Display Units columns
                        widget.setEnabled(True)
                        widget.setStyleSheet("")
            # Platinum RTD
            elif type == 2:
                for col in range(2, 7):
                    widget = self.sensor_layout.itemAtPosition(row, col).widget()
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
                    widget = self.sensor_layout.itemAtPosition(row, col).widget()
                    widget.setEnabled(True)
                    widget.setStyleSheet("")

            else:
                # Only enable type column
                widget = self.sensor_layout.itemAtPosition(row, 2).widget()
                widget.setEnabled(True)
                widget.setStyleSheet("")
        else:
            for col in range(2, 7):
                widget = self.sensor_layout.itemAtPosition(row, col).widget()
                widget.setEnabled(False)
                widget.setStyleSheet("QComboBox { color: darkgray; }")

        

    def read_sensor_setup(self):
        try:
            for row in range(8):
                input_number = row + 1
                message = f"INTYPE? {input_number}\n"
                self.ser.write(message.encode())
                response = self.ser.read(1024).decode().strip()

                # Parse the response
                sensor_type, autorange, range_val, current_reversal, units, enabled = response.split(",")

                # # Update the QComboBoxes based on the parsed values
                power_combo_box =self.sensor_layout.itemAtPosition(row + 1, 0).widget()
                type_combo_box = self.sensor_layout.itemAtPosition(row + 1, 2).widget()
                autorange_combo_box = self.sensor_layout.itemAtPosition(row + 1, 4).widget()
                range_combo_box = self.sensor_layout.itemAtPosition(row + 1, 5).widget()
                current_reversal_combo_box = self.sensor_layout.itemAtPosition(row + 1, 3).widget()
                display_units_combo_box = self.sensor_layout.itemAtPosition(row + 1, 6).widget()

                # Update Power combo box
                power_combo_box.setCurrentIndex(int(enabled))

                # Update Type combo box
                type_combo_box.setCurrentIndex(int(sensor_type)-1)

                # Update Autorange combo box
                autorange_combo_box.setCurrentIndex(int(autorange))

                # Update Current Reversal combo box
                current_reversal_combo_box.setCurrentIndex(int(current_reversal))

                # Update Display Units combo box
                display_units_combo_box.setCurrentIndex(int(units)-1)

                if int(enabled) == 1:
                    # Diode
                    if int(sensor_type) == 1:
                        self.table_widget.setItem(row, 3, QTableWidgetItem("10 µA"))
                        range_combo_box.clear()
                        range_combo_box.addItems(["7.5 V (10 µA)"])
                        range_combo_box.setCurrentIndex(int(range_val))
                        for col in range(2, 7):
                            widget = self.sensor_layout.itemAtPosition(input_number, col).widget()
                            if col in [2, 6]:  # Type and Display Units columns
                                widget.setEnabled(True)
                                widget.setStyleSheet("")
                            else:
                                widget.setEnabled(False)
                                widget.setStyleSheet("QComboBox { color: darkgray; }")
                    # Platinum RTD
                    elif int(sensor_type) == 2:
                        self.table_widget.setItem(row, 3, QTableWidgetItem("1 mA"))
                        range_combo_box.clear()
                        range_combo_box.addItems(["1 kΩ (1 mA)"])
                        range_combo_box.setCurrentIndex(int(range_val))
                        for col in range(2, 7):
                            widget = self.sensor_layout.itemAtPosition(input_number, col).widget()
                            if col in [2, 3, 6]:  # Type, Current Reversal, and Display Units columns
                                widget.setEnabled(True)
                                widget.setStyleSheet("")
                            else:
                                widget.setEnabled(False)
                                widget.setStyleSheet("QComboBox { color: darkgray; }")
                    # NTC RTD
                    elif int(sensor_type) == 3:
                        range_combo_box.clear()
                        range_combo_box.addItems(["10 Ω (1 mA)", "30 Ω (300 µA)", "100 Ω (100 µA)",
                        "300 Ω (30 µA)", "1 kΩ (10 µA)", "3 kΩ (3 µA)", "10 kΩ (1 µA)",
                        "30 kΩ (300 nA)", "100 kΩ (100 nA)"])
                        range_combo_box.setCurrentIndex(int(range_val))
                        excitation = range_combo_box.currentText()
                        # Extracting the part between parentheses
                        start_index = excitation.find('(') + 1
                        end_index = excitation.find(')', start_index)
                        parsed_excitation = excitation[start_index:end_index]
                        self.table_widget.setItem(row, 3, QTableWidgetItem(parsed_excitation))
                        for col in range(2, 7):
                            widget = self.sensor_layout.itemAtPosition(input_number, col).widget()
                            widget.setEnabled(True)
                            widget.setStyleSheet("")

                    else:
                        range_combo_box.clear()
                        range_combo_box.addItems([""])
                        range_combo_box.setCurrentIndex(int(range_val))
                        # Only enable type column
                        for col in range(3, 7):
                            widget = self.sensor_layout.itemAtPosition(input_number, col).widget()
                            widget.setEnabled(False)
                            widget.setStyleSheet("QComboBox { color: darkgray; }")
                        widget = self.sensor_layout.itemAtPosition(input_number, 2).widget()
                        widget.setEnabled(True)
                        widget.setStyleSheet("")
                else:
                    range_combo_box.clear()
                    range_combo_box.addItems([""])
                    range_combo_box.setCurrentIndex(int(range_val))
                    for col in range(2, 7):
                        widget = self.sensor_layout.itemAtPosition(input_number, col).widget()
                        widget.setEnabled(False)
                        widget.setStyleSheet("QComboBox { color: darkgray; }")

        except serial.SerialException as e:
                print(f"Error: {e}")

    def handle_curve_change(self, index):
        try:
            sender = self.sender()
            input = 0
            i = 1
            for combobox in self.curve_comboboxes:
                if combobox == sender:
                    input = i
                    break
                i +=1
            sensor_type_box = self.sensor_layout.itemAtPosition(input, 2).widget()
            sensor_current_box = self.sensor_layout.itemAtPosition(input, 3).widget()
            sensor_autorange_box = self.sensor_layout.itemAtPosition(input, 4).widget()
            sensor_range_box = self.sensor_layout.itemAtPosition(input, 5).widget()
            sensor_unit_box = self.sensor_layout.itemAtPosition(input, 6).widget()
            file = ""
            name = ""
            serial = ""
            format = 0
            coefficient = 0
            index = sender.currentIndex()
            match index:
                case 0:
                    file = "LSCI_DT600.txt"
                    name = "LSCI_DT-600"
                    serial = "Standard C"
                    format = 2
                    limit = 500
                    coefficient = 1
                case 1:
                    file = "LSCI_DT400.txt"
                    name = "LSCI_DT-400"
                    serial = "Standard C"
                    format = 2
                    limit = 475
                    coefficient = 1
                case 2:
                    file = "LSCI_PT100.txt"
                    name = "LSCI_PT-100"
                    serial = "STANDARD"
                    format = 3
                    limit = 800
                    coefficient = 2
                case 3:
                    file = "IEC_PT100_RTD.txt"
                    name = "IEC_PT100_RTD"
                    serial = "STANDARD"
                    format = 3
                    limit = 800
                    coefficient = 2                
                case 4:
                    file = "IEC_PT1000_RTD.txt"
                    name = "IEC_PT1000_RTD"
                    serial = "STANDARD"
                    format = 3
                    limit = 800
                    coefficient = 2
                case 5:
                    file = "SIMULATED_SENSO.txt"
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
                try:
                    with open(file, "r") as opened_file:
                        current_index = 0
                        for line in opened_file:
                            current_index+=1
                            values = line.strip().split(',')
                            unit, temp = map(float, values)
                            message = f"CRVPT {input},{current_index},{unit},{temp}\n"
                            self.ser.write(message.encode())
                except FileNotFoundError:
                    print("File not found.")

                except ValueError:
                    print("Error parsing data.")

                except Exception as e:
                    print("An error occurred:", e)
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
    window = TemperatureWindow()
    window.show()
    app.exec()
