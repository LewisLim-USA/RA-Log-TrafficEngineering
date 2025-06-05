#!/bin/bash

# Description: Run the MPU6050 sensor script and save logs for debugging

echo "Running smbus_example.py..."
python3 smbus_example.py > debug_output.log 2>&1

# Notify when finished
echo "Done. Check debug_output.log for sensor output and errors."
