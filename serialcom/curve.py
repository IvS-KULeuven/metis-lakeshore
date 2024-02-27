def read_curves(main_window):
    try:
        for row in range(8):
            input_number = row + 1
            message = f"CRVHDR? {input_number}\n"
            main_window.ser.write(message.encode())
            response = main_window.ser.read(1024).decode().strip().split(",")[:5]
            name = response[0].strip()
            if (name == "LSCI_DT-600"):
                main_window.curve_ui.curve_comboboxes[row].setCurrentIndex(0)
            elif (name == "LSCI_DT-400"):
                main_window.curve_ui.curve_comboboxes[row].setCurrentIndex(1)
            elif (name == "LSCI_PT-100"):
                main_window.curve_ui.curve_comboboxes[row].setCurrentIndex(2)
            elif (name == "IEC_PT100_RTD"):
                main_window.curve_ui.curve_comboboxes[row].setCurrentIndex(3)
            elif (name == "IEC_PT1000_RTD"):
                main_window.curve_ui.curve_comboboxes[row].setCurrentIndex(4)
            elif (name == "Simulated Senso"):
                main_window.curve_ui.curve_comboboxes[row].setCurrentIndex(5)
            else:
                main_window.curve_ui.curve_comboboxes[row].setCurrentIndex(-1)
    except Exception as e:
        print(f"Error: {e}")