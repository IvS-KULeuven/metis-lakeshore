from PySide6.QtWidgets import QTableWidgetItem

def read_temperature(main_window):
    try:
        # Write data to the port to ask temperature in Kelvin
        message = "KRDG? 0\n"
        main_window.ser.write(message.encode())

        # Read temperature data from the port
        data = main_window.ser.read(1024).decode().strip()
        temperatures = data.split(",")[:8]

        # Update table with formatted temperatures
        for row, temp in enumerate(temperatures):
            if(main_window.sensor_ui.power_comboboxes[row].currentIndex() == 1):  #if power is on
                formatted_temp = temp.lstrip('+')  # Remove leading '+'
                if  '.' in formatted_temp:
                    formatted_temp = formatted_temp.lstrip('0')  # Remove leading '0's
                if len(formatted_temp) > 0 and formatted_temp[0] == ".":
                    formatted_temp = '0' + formatted_temp
                formatted_temp = formatted_temp + " K"
                if formatted_temp == '0.00000 K':
                    message = f"RDGST? {row+1}\n"
                    main_window.ser.write(message.encode())
                    response = main_window.ser.read(1024).decode().strip()
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
                main_window.temperature_ui.table.setItem(row, 1, QTableWidgetItem(formatted_temp if formatted_temp != '0.00000 K' else '0 K'))
            else:
                main_window.temperature_ui.table.setItem(row, 1, QTableWidgetItem(""))

    except Exception as e:
        print(f"Error: {e}")

def read_sensor_units(main_window):
    try:
        # Write query to the port to ask sensor units
        message = "SRDG? 0\n"
        main_window.ser.write(message.encode())

        # Read sensor units data from the port
        data = main_window.ser.read(1024).decode().strip()
        sensor_units = data.split(",")[:8]

        # Update table with sensor units
        for row, unit in enumerate(sensor_units):
            if(main_window.sensor_ui.power_comboboxes[row].currentIndex() == 1): # If power is on
                unit = unit.lstrip('+')  # Remove leading '+'
                if '.' in unit:
                    unit = unit.lstrip('0')  # Remove leading '0's
                if len(unit) > 0 and unit[0] == ".":
                    unit = '0' + unit
                if(main_window.sensor_ui.type_comboboxes[row].currentIndex() == 0):
                    unit = unit + " V"
                else:
                    unit = unit + " Ω"
                main_window.temperature_ui.table.setItem(row, 2, QTableWidgetItem(unit if (unit != '0.000 V' and unit != '0.000 Ω') else '0'))
                set_excitation(main_window,row)
                calculate_power(main_window,row)
            else:
                main_window.temperature_ui.table.setItem(row, 2, QTableWidgetItem(""))
                main_window.temperature_ui.table.setItem(row, 3, QTableWidgetItem(""))
                main_window.temperature_ui.table.setItem(row, 4, QTableWidgetItem(""))

    except Exception as e:
        print(f"Error: {e}")

def calculate_power(main_window, row):
    try:
        sensor_text = main_window.temperature_ui.table.item(row, 2).text()
        excitation_text =main_window.temperature_ui.table.item(row, 3).text()

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
        main_window.temperature_ui.table.setItem(row, 4, QTableWidgetItem(power))

    except Exception as e:
        print(f"Error: {e}")

def set_excitation(main_window, row):
    range_combo_box = main_window.sensor_ui.layout.itemAtPosition(row+1, 5).widget()
    excitation = range_combo_box.currentText()
    # Extracting the part between parentheses
    start_index = excitation.find('(') + 1
    end_index = excitation.find(')', start_index)
    parsed_excitation = excitation[start_index:end_index]
    main_window.temperature_ui.table.setItem(row, 3, QTableWidgetItem(parsed_excitation))