def read_address(main_window):
    try:
        message = "ADDR?\n"
        main_window.ser.write(message.encode())
        address = main_window.ser.read(1024).decode().strip()
        main_window.profibus_ui.address_line_edit.setText(address)

    except Exception as e:
        print(f"Error: {e}")

def read_slot_count(main_window):
    try:
        message = "PROFINUM?\n"
        main_window.ser.write(message.encode())
        value = int(main_window.ser.read(1024).decode().strip())
        main_window.profibus_ui.slot_combobox.setCurrentIndex(value)

    except Exception as e:
        print(f"Error: {e}")

def read_slots(main_window):
    try:
        for row in range(8):
            input_number = row + 1
            message = f"PROFISLOT? {input_number}\n"
            main_window.ser.write(message.encode())
            data = main_window.ser.read(1024).decode().strip().split(",")[:2]
            main_window.profibus_ui.channel_comboboxes[row].setCurrentIndex(int(data[0])-1)
            main_window.profibus_ui.units_comboboxes[row].setCurrentIndex(int(data[1])-1)

    except Exception as e:
        print(f"Error: {e}")