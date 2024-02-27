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

def handle_address_change(main_window):
    new_address = int(main_window.profibus_ui.address_line_edit.text())
    message = f"ADDR {new_address}\n"
    main_window.ser.write(message.encode())

def handle_slot_count_change(main_window):
    selected_slot = main_window.profibus_ui.slot_combobox.currentIndex()
    message = f"PROFINUM {selected_slot}\n"
    main_window.ser.write(message.encode())

def handle_channel_unit_change(main_window):
    sender_combobox = main_window.sender()
    row = main_window.profibus_ui.layout.getItemPosition(main_window.profibus_ui.layout.indexOf(sender_combobox))[0]
    input_number = row - 3  # Offset by 3 to account for the header rows

    channel_index = main_window.profibus_ui.channel_comboboxes[input_number-1].currentIndex()
    unit_index = main_window.profibus_ui.units_comboboxes[input_number-1].currentIndex()

    main_window.handle_comboboxes_change(input_number, channel_index, unit_index)

def handle_comboboxes_change(main_window, input_number, channel_index, unit_index):
    message = f"PROFISLOT {input_number},{channel_index+1},{unit_index+1}\n"
    main_window.ser.write(message.encode())