from PySide6.QtWidgets import QTableWidgetItem

def read_input_names(main_window):
        try:
            for row in range(8):
                input_number = row + 1
                message = f"INNAME? {input_number}\n"
                main_window.ser.write(message.encode())
                name = main_window.ser.read(1024).decode().strip()
                main_window.temperature_ui.table.setItem(row, 0, QTableWidgetItem(name))
                main_window.sensor_ui.name_line_edits[row].setText(name)
                main_window.curve_ui.name_labels[row].setText(name)
        except Exception as e:
            print(f"Error: {e}")


def read_sensor_setup(main_window):
        try:
            for row in range(8):
                input_number = row + 1
                message = f"INTYPE? {input_number}\n"
                main_window.ser.write(message.encode())
                response = main_window.ser.read(1024).decode().strip()

                # Parse the response
                sensor_type, autorange, range_val, current_reversal, units, enabled = response.split(",")

                # # Update the QComboBoxes based on the parsed values
                power_combo_box =main_window.sensor_ui.layout.itemAtPosition(row + 1, 0).widget()
                type_combo_box = main_window.sensor_ui.layout.itemAtPosition(row + 1, 2).widget()
                autorange_combo_box = main_window.sensor_ui.layout.itemAtPosition(row + 1, 4).widget()
                range_combo_box = main_window.sensor_ui.layout.itemAtPosition(row + 1, 5).widget()
                current_reversal_combo_box = main_window.sensor_ui.layout.itemAtPosition(row + 1, 3).widget()
                display_units_combo_box = main_window.sensor_ui.layout.itemAtPosition(row + 1, 6).widget()

                # Update Power combo box
                power_combo_box.setCurrentIndex(int(enabled))

                # Update Type combo box
                type_combo_box.setCurrentIndex(int(sensor_type)-1)

                # Update Autorange combo box
                autorange_combo_box.setCurrentIndex(int(autorange))

                # Update Current Reversal combo boxAML is a superset of JSON, so we can utilize JSON style sequences and maps in our constructs:
                current_reversal_combo_box.setCurrentIndex(int(current_reversal))

                # Update Display Units combo box
                display_units_combo_box.setCurrentIndex(int(units)-1)

                if int(enabled) == 1:
                    # Diode
                    if int(sensor_type) == 1:
                        main_window.temperature_ui.table.setItem(row, 3, QTableWidgetItem("10 µA"))
                        range_combo_box.clear()
                        range_combo_box.addItems(["7.5 V (10 µA)"])
                        range_combo_box.setCurrentIndex(int(range_val))
                        for col in range(2, 7):
                            widget = main_window.sensor_ui.layout.itemAtPosition(input_number, col).widget()
                            if col in [2, 6]:  # Type and Display Units columns
                                widget.setEnabled(True)
                                widget.setStyleSheet("")
                            else:
                                widget.setEnabled(False)
                                widget.setStyleSheet("QComboBox { color: darkgray; }")
                    # Platinum RTD
                    elif int(sensor_type) == 2:
                        main_window.temperature_ui.table.setItem(row, 3, QTableWidgetItem("1 mA"))
                        range_combo_box.clear()
                        range_combo_box.addItems(["1 kΩ (1 mA)"])
                        range_combo_box.setCurrentIndex(int(range_val))
                        for col in range(2, 7):
                            widget = main_window.sensor_ui.layout.itemAtPosition(input_number, col).widget()
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
                        for col in range(2, 7):
                            widget = main_window.sensor_ui.layout.itemAtPosition(input_number, col).widget()
                            widget.setEnabled(True)
                            widget.setStyleSheet("")

                    else:
                        range_combo_box.clear()
                        range_combo_box.addItems([""])
                        range_combo_box.setCurrentIndex(int(range_val))
                        # Only enable type column
                        for col in range(3, 7):
                            widget = main_window.sensor_ui.layout.itemAtPosition(input_number, col).widget()
                            widget.setEnabled(False)
                            widget.setStyleSheet("QComboBox { color: darkgray; }")
                        widget = main_window.sensor_ui.layout.itemAtPosition(input_number, 2).widget()
                        widget.setEnabled(True)
                        widget.setStyleSheet("")
                else:
                    range_combo_box.clear()
                    range_combo_box.addItems([""])
                    range_combo_box.setCurrentIndex(int(range_val))
                    for col in range(2, 7):
                        widget = main_window.sensor_ui.layout.itemAtPosition(input_number, col).widget()
                        widget.setEnabled(False)
                        widget.setStyleSheet("QComboBox { color: darkgray; }")

        except Exception as e:
                print(f"Error: {e}")

def handle_type_change(main_window, combobox, i):
    # Get the row number of the combo box in the layout
    row = i+1

    # Get the selected type
    selected_type = combobox.currentText()

    # Get the relevant combo boxes for the current row
    current_reversal_combo_box = main_window.sensor_ui.layout.itemAtPosition(row, 3).widget()
    autorange_combo_box = main_window.sensor_ui.layout.itemAtPosition(row, 4).widget()
    range_combo_box = main_window.sensor_ui.layout.itemAtPosition(row, 5).widget()
    units_combo_box = main_window.sensor_ui.layout.itemAtPosition(row, 6).widget()
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
    power = main_window.sensor_ui.layout.itemAtPosition(row, 0).widget().currentIndex()
    type = main_window.sensor_ui.layout.itemAtPosition(row, 2).widget().currentIndex() +1
    current_reversal = main_window.sensor_ui.layout.itemAtPosition(row, 3).widget().currentIndex()
    autorange = main_window.sensor_ui.layout.itemAtPosition(row, 4).widget().currentIndex()
    selected_range = main_window.sensor_ui.layout.itemAtPosition(row, 5).widget().currentIndex()
    unit = main_window.sensor_ui.layout.itemAtPosition(row, 6).widget().currentIndex() +1

    message = f"INTYPE {row},{type},{autorange},{selected_range},{current_reversal},{unit},{power}\n"
    main_window.ser.write(message.encode())

def sensor_connect_type_combobox(combobox, main_window, index):
    combobox.currentIndexChanged.connect(lambda: handle_type_change(main_window, combobox, index))