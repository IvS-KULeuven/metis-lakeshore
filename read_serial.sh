#!/bin/bash

# Check if socat is installed
command -v socat >/dev/null 2>&1 || { echo >&2 "socat is required but it's not installed. Aborting."; exit 1; }

# Check if the serial port exists
if [ ! -c /dev/ttyUSB0 ]; then
    echo "Serial port /dev/ttyUSB0 not found."
    exit 1
fi

# Specify the file to write data to
output_file="serial_data.txt"

# Start socat to duplicate data from the serial port to the output file
socat -d -d pty,raw,echo=0,ignoreeof,b115200,nonblock,link=/dev/virtualtty0 /dev/ttyUSB0,raw,echo=0,b115200,nonblock,ignoreeof > "$output_file"
