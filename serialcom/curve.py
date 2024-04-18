def read_curves(main_window, signal_manager):
    try:
        for row in range(8):
            input_number = row + 1
            message = f"CRVHDR? {input_number}\n"
            main_window.ser.write(message.encode())
            response = main_window.ser.read(1024).decode().strip().split(",")[:5]
            name = response[0].strip()
            if (name == "LSCI_DT-600"):
                signal_manager.update_ui(f"curve_ui.curve_comboboxes[{row}]", "setCurrentIndex", 0)
            elif (name == "LSCI_DT-400"):
                signal_manager.update_ui(f"curve_ui.curve_comboboxes[{row}]", "setCurrentIndex", 1)
            elif (name == "LSCI_PT-100"):
                signal_manager.update_ui(f"curve_ui.curve_comboboxes[{row}]", "setCurrentIndex", 2)
            elif (name == "IEC_PT100_RTD"):
                signal_manager.update_ui(f"curve_ui.curve_comboboxes[{row}]", "setCurrentIndex", 3)
            elif (name == "IEC_PT1000_RTD"):
                signal_manager.update_ui(f"curve_ui.curve_comboboxes[{row}]", "setCurrentIndex", 4)
            elif (name == "Simulated Senso"):
                signal_manager.update_ui(f"curve_ui.curve_comboboxes[{row}]", "setCurrentIndex", 5)
            else:
                signal_manager.update_ui(f"curve_ui.curve_comboboxes[{row}]", "setCurrentIndex", -1)
    except Exception as e:
        print(f"Error: {e}")

def handle_delete_curve(main_window, i):
    message = f"CRVDEL {i+1}\n"
    main_window.ser.write(message.encode())
    main_window.curve_ui.curve_comboboxes[i].setCurrentIndex(-1)

def handle_curve_change(main_window, combobox, i):
        try:
            input = i +1
            sensor_type_box = main_window.sensor_ui.layout.itemAtPosition(input, 2).widget()
            sensor_current_box = main_window.sensor_ui.layout.itemAtPosition(input, 3).widget()
            sensor_autorange_box = main_window.sensor_ui.layout.itemAtPosition(input, 4).widget()
            sensor_range_box = main_window.sensor_ui.layout.itemAtPosition(input, 5).widget()
            sensor_unit_box = main_window.sensor_ui.layout.itemAtPosition(input, 6).widget()
            file = ""
            name = ""
            serial = ""
            format = 0
            coefficient = 0
            index = combobox.currentIndex()
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
                main_window.ser.write(message.encode())
                message = f"CRVHDR {input},{name},{serial},{format},{limit},{coefficient}\n"
                main_window.ser.write(message.encode())
                with open(file, "r") as opened_file:
                    current_index = 0
                    for line in opened_file:
                        current_index+=1
                        values = line.strip().split(',')
                        unit, temp = map(float, values)
                        message = f"CRVPT {input},{current_index},{unit},{temp}\n"
                        main_window.ser.write(message.encode())

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

def curve_connect_delete_button(button, main_window, index):
    button.clicked.connect(lambda: handle_delete_curve(main_window, index))

def curve_connect_curve_combobox(combobox, main_window, index):
    combobox.currentIndexChanged.connect(lambda: handle_curve_change(main_window, combobox, index))