def read_general_information(main_window):
    try:
        # Retrieve and display module name
        module_message = "MODNAME?\n"
        main_window.ser.write(module_message.encode())
        module_name = main_window.ser.read(1024).decode().strip()
        main_window.general_ui.module_name_label.setText(module_name)

        # Send command to get general information
        message = "*IDN?\n"
        main_window.ser.write(message.encode())

        # Read response and split into components
        data = main_window.ser.read(1024).decode().strip()
        components = data.split(",")

        # Update labels with general information
        main_window.general_ui.serial_number_label.setText(components[2])
        main_window.general_ui.firmware_version_label.setText(components[3])

    except Exception as e:
        print(f"Error: {e}")


def read_brightness(main_window):
    try:
        # Retrieve and display brightness
        message = "BRIGT?\n"
        main_window.ser.write(message.encode())
        brightness_value = int(main_window.ser.read(1024).decode().strip())

        # Set the current index of the combo box based on the brightness value
        main_window.general_ui.brightness_combobox.setCurrentIndex(brightness_value)

    except Exception as e:
        print(f"Error: {e}")