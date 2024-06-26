import serial
import serial.tools.list_ports
from serialcom.general import read_general_information, read_brightness, handle_module_name_change, handle_brightness_change, handle_restore_factory_settings
from serialcom.profibus import read_address, read_slot_count, read_slots, handle_address_change, handle_slot_count_change, profibus_connect_combobox
from serialcom.sensor import read_input_names, read_sensor_setup, sensor_connect_type_combobox, sensor_connect_name_edit, sensor_connect_power_combobox, sensor_connect_combobox
from serialcom.curve import read_curves, curve_connect_delete_button, curve_connect_curve_combobox
from PySide6.QtCore import QThread
from thread.worker import Worker
from thread.timer_worker import TimerWorker

def find_connected_devices(main_window):
        try:
            # Clear stuff
            main_window.connection_ui.connection_combobox.clear()
            main_window.connection_ui.devices_list.clear()
            
            # Scan USB ports for connected devices
            devices = serial.tools.list_ports.comports()

            # Add devices to the combobox
            for device in devices:
                with serial.Serial(device.device) as ser:
                    device_str = remove_duplicate_parts(str(device))
                    main_window.connection_ui.connection_combobox.addItem(device_str)
                    main_window.connection_ui.devices_list.append(device)
        except Exception as e:
            print(f"Error: {e}")

def remove_duplicate_parts(input_string):
    parts = input_string.split(" - ")
    if len(parts) == 3 and parts[1] == parts[2]:
        return parts[0] + " - " + parts[1]
    else:
        return input_string


def handle_disconnect(main_window):
    if main_window.ser == '':
        return
    try:
        # Perform cleanup when the temperature_worker has finished its task
        if main_window.timer_worker_thread and main_window.timer_worker_thread.isRunning():
            main_window.timer_worker_thread.quit()
            main_window.timer_worker_thread.wait()
            main_window.timer_worker_thread = None
            main_window.timer_worker = None

        main_window.ser.close()
        
        # Disconnect signals
        main_window.general_ui.module_name_label.editingFinished.disconnect()
        main_window.profibus_ui.address_line_edit.editingFinished.disconnect()
        main_window.general_ui.brightness_combobox.currentIndexChanged.disconnect()
        main_window.profibus_ui.slot_combobox.currentIndexChanged.disconnect()
        main_window.general_ui.restore_button.clicked.disconnect()

        # Disconnect signals for comboboxes and others
        for i in range(8):
            main_window.profibus_ui.channel_comboboxes[i].currentIndexChanged.disconnect()
            main_window.profibus_ui.units_comboboxes[i].currentIndexChanged.disconnect()
            main_window.sensor_ui.type_comboboxes[i].currentIndexChanged.disconnect()
            main_window.sensor_ui.power_comboboxes[i].currentIndexChanged.disconnect()
            main_window.sensor_ui.name_line_edits[i].editingFinished.disconnect()
            main_window.curve_ui.name_labels[i].editingFinished.disconnect()
            main_window.sensor_ui.current_reversal_comboboxes[i].currentIndexChanged.disconnect()
            main_window.sensor_ui.autorange_comboboxes[i].currentIndexChanged.disconnect()
            main_window.sensor_ui.range_comboboxes[i].currentIndexChanged.disconnect()
            main_window.sensor_ui.display_units_comboboxes[i].currentIndexChanged.disconnect()
            main_window.curve_ui.delete_buttons[i].clicked.disconnect()
            main_window.curve_ui.curve_comboboxes[i].currentIndexChanged.disconnect()

        main_window.connection_ui.status_label.setText("<b>Status: </b>        Disconnected")
    except Exception as e:
        print(f"Error: {e}")


def read_serial(main_window, signal_manager):
        try:
            i = main_window.connection_ui.connection_combobox.currentIndex()
            device = main_window.connection_ui.devices_list[i]
            main_window.port = device.device
            main_window.ser = serial.Serial(main_window.port, main_window.baudrate, timeout=main_window.timeout)
            read_general_information(main_window, signal_manager)
            read_brightness(main_window, signal_manager)
            read_address(main_window, signal_manager)
            read_slot_count(main_window, signal_manager)
            read_slots(main_window, signal_manager)
            read_input_names(main_window, signal_manager)
            read_curves(main_window, signal_manager)
            read_sensor_setup(main_window, signal_manager)
        except Exception as e:
            print(f"Error: {e}")
    

def connect_signals(main_window, signal_manager):
    try:
        # Connect signals
        main_window.general_ui.module_name_label.editingFinished.connect(lambda: handle_module_name_change(main_window))
        main_window.profibus_ui.address_line_edit.editingFinished.connect(lambda: handle_address_change(main_window))
        main_window.general_ui.brightness_combobox.currentIndexChanged.connect(lambda: handle_brightness_change(main_window))
        main_window.profibus_ui.slot_combobox.currentIndexChanged.connect(lambda: handle_slot_count_change(main_window))
        main_window.general_ui.restore_button.clicked.connect(lambda: handle_restore_factory_settings(main_window))

        # Connect signals for comboboxes and others
        for i in range(8):
            profibus_connect_combobox(main_window.profibus_ui.channel_comboboxes[i],main_window, i)
            profibus_connect_combobox(main_window.profibus_ui.units_comboboxes[i],main_window, i)
            sensor_connect_type_combobox(main_window.sensor_ui.type_comboboxes[i], main_window, i)
            sensor_connect_power_combobox(main_window.sensor_ui.power_comboboxes[i], main_window, i)
            sensor_connect_name_edit(main_window.sensor_ui.name_line_edits[i], main_window, i)
            sensor_connect_name_edit(main_window.curve_ui.name_labels[i], main_window, i)
            sensor_connect_combobox(main_window.sensor_ui.current_reversal_comboboxes[i], main_window, i)
            sensor_connect_combobox(main_window.sensor_ui.autorange_comboboxes[i], main_window, i)
            sensor_connect_combobox(main_window.sensor_ui.range_comboboxes[i], main_window, i)
            sensor_connect_combobox(main_window.sensor_ui.display_units_comboboxes[i], main_window, i)
            curve_connect_delete_button(main_window.curve_ui.delete_buttons[i], main_window, i)
            curve_connect_curve_combobox(main_window.curve_ui.curve_comboboxes[i], main_window, i)
        signal_manager.update_ui("connection_ui.status_label", "setText", "<b>Status: </b>        Connected")
    except Exception as e:
        print(f"Error: {e}")

def handle_connect(main_window, signal_manager):
    try:
        if not main_window.worker_thread or not main_window.worker_thread.isRunning():
            # Create new worker and thread
            main_window.worker = Worker(main_window, signal_manager)
            main_window.worker_thread = QThread()
            main_window.worker.moveToThread(main_window.worker_thread)
            main_window.worker.finished_signal.connect(lambda: handle_worker_finished(main_window, signal_manager))
            main_window.worker_thread.started.connect(main_window.worker.run)
            main_window.worker.start_timers_signal.connect(lambda: start_timer(main_window, signal_manager))
            main_window.worker_thread.start()
    except Exception as e:
        print(f"Error: {e}")

def handle_worker_finished(main_window, signal_manager):
    try:
        # Perform cleanup when the worker has finished its task
        if main_window.worker_thread and main_window.worker_thread.isRunning():
            main_window.worker_thread.quit()
            main_window.worker_thread.wait()
            main_window.worker_thread = None
            main_window.worker = None
        connect_signals(main_window, signal_manager)
    except Exception as e:
        print(f"Error: {e}")

def start_timer(main_window, signal_manager):
    # Create new timer_worker and thread
    main_window.timer_worker = TimerWorker(main_window, signal_manager)
    main_window.timer_worker_thread = QThread()
    main_window.timer_worker.moveToThread(main_window.timer_worker_thread)
    main_window.timer_worker_thread.started.connect(main_window.timer_worker.run)
    main_window.timer_worker_thread.start()