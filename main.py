import PySide6
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QSizePolicy, QLabel, QGridLayout, QLineEdit, QFrame, QComboBox
from PySide6.QtCore import Qt, QTimer
import serial

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

        # Profibus communication section
        self.profibus_label = QLabel("<b>PROFIBUS communication</b>")
        self.profibus_label.setStyleSheet("font-size: 14pt;")

        # Add sections to general layout
        self.left_layout.addWidget(self.general_label)
        self.left_layout.addWidget(self.general_section_frame)
        self.left_layout.addWidget(self.profibus_label)

        # Right layout for temperature table
        self.right_layout = QVBoxLayout()
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setRowCount(8)
        self.table_widget.setHorizontalHeaderLabels(["Name", "Temperature", "Sensor units", "Excitation", "Power"])

        # Populate table with sample data
        for row in range(8):
            self.table_widget.setItem(row, 0, QTableWidgetItem(""))  # Set item in first column
            self.table_widget.setItem(row, 1, QTableWidgetItem("0"))  # Set item in second column
            self.table_widget.setItem(row, 2, QTableWidgetItem(""))  # Set item in third column
            self.table_widget.setItem(row, 3, QTableWidgetItem(""))  # Set item in fourth column
            self.table_widget.setItem(row, 4, QTableWidgetItem(""))  # Set item in fifth column

        # Set size policy to expand vertically
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set vertical header to resize to contents
        self.table_widget.verticalHeader().setSectionResizeMode(PySide6.QtWidgets.QHeaderView.ResizeToContents)

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
        self.read_temperature()
        self.read_sensor_units()
        self.read_curves()

        # Start timer for updating temperature
        self.timer = QTimer(self)
        self.timer.setInterval(10000)  # Update every 10 seconds
        self.timer.timeout.connect(self.read_temperature)
        self.timer.start()

        # Connect signals
        self.module_name_label.editingFinished.connect(self.handle_module_name_change)
        self.brightness_combobox.currentIndexChanged.connect(self.handle_brightness_change)

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
        except serial.SerialException as e:
            print(f"Error: {e}")

    def read_temperature(self):
        try:
            # Write data to the port to ask temperature in Kelvin
            message = "KRDG? 0\n"
            self.ser.write(message.encode())

            # Read temperature data from the port
            data = self.ser.read(1024).decode().strip()  # Read up to 1024 bytes and decode
            temperatures = data.split(",")[:8]  # Extract the first 8 temperatures

            # Update table with formatted temperatures
            for row, temp in enumerate(temperatures):
                formatted_temp = temp.lstrip('+')  # Remove leading '+'
                if formatted_temp.startswith('0') and '.' in formatted_temp:
                    formatted_temp = formatted_temp.lstrip('0')  # Remove leading '0's except for '0.0'
                formatted_temp = formatted_temp + " K"
                self.table_widget.setItem(row, 1, QTableWidgetItem(formatted_temp if formatted_temp != '.00000 K' else '0 K'))

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
                unit = unit.lstrip('+')  # Remove leading '+'
                if '.' in unit:
                    unit = unit.lstrip('0')  # Remove leading '0's
                unit = '0' + unit
                self.table_widget.setItem(row, 2, QTableWidgetItem(unit if unit != '0.000' else '0'))

        except serial.SerialException as e:
            print(f"Error: {e}")

    def read_curves(self):
        try:
            for row in range(8):
                input_number = row + 1
                message = f"CRVHDR? {input_number}\n"
                self.ser.write(message.encode())
                value = self.ser.read(1024).decode().strip().split(",")[2]
                excitation = '10µA' if value == '2' else '1mA' if value == '3' else ''
                self.table_widget.setItem(row, 3, QTableWidgetItem(excitation))

        except serial.SerialException as e:
            print(f"Error: {e}")

    def handle_module_name_change(self):
        new_name = self.module_name_label.text()
        message = f"MODNAME {new_name}\n"
        self.ser.write(message.encode())

    def handle_brightness_change(self, index):
        selected_brightness = self.brightness_combobox.currentIndex()
        message = f"BRIGT {selected_brightness}\n"
        self.ser.write(message.encode())

if __name__ == "__main__":
    app = QApplication([])
    window = TemperatureWindow()
    window.show()
    app.exec()
