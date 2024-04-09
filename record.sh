#!/bin/bash

# Check if filename is provided as parameter
if [ -z "$1" ]; then
    echo "Usage: ./script.sh <filename>"
    exit 1
fi

filename="$1"

# IP address and password of your Solax solar inverter
ip_address="192.168.178.35"
password="SNXXXXXXXX"

# Continuous loop to send POST requests and append response to file
while true; do 
    curl -X POST http://$ip_address/ -d "optType=ReadRealTimeData&pwd=$password" >> "$filename"
    date >> "$filename"
    sleep 300
done
