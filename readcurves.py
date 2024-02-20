import serial

# Configure serial port settings
port = '/dev/ttyUSB0'
baudrate = 115200
timeout = 1

# Open the serial port
ser = serial.Serial(port, baudrate, timeout=timeout)

try:
    with open("new_file.txt", "w") as file:
        for i in range(200):
            index = i+1
            message = f"CRVPT? 1, {index}\n"
            ser.write(message.encode())
            name = ser.read(1024).decode().strip()
            file.write(name + "\n")
            
except serial.SerialException as e:
    print(f"Error: {e}")

finally:
    # Close the serial port
    ser.close()