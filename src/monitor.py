import os
import subprocess
import time
from datetime import datetime

def ping_device(ip):
    try:
        result = subprocess.check_output(
            ["ping", "-c", "1", ip],
            universal_newlines=True
        )

        # Extract response time
        if "time=" in result:
            response_time = result.split("time=")[1].split(" ")[0]
        else:
            response_time = "N/A"

        return {
            "status": "ONLINE",
            "response_time": response_time
        }

    except:
        return {
            "status": "OFFLINE",
            "response_time": "N/A"
        }

# Devices to monitor
devices = {
    "Localhost": "127.0.0.1",
    "Google DNS": "8.8.8.8",
    "Ubuntu VM": "192.168.30.3",
    "Test Offline Device": "10.255.255.1"
}

# Store previous statuses
previous_status = {}

while True:
    print("\n--- Network Monitoring ---\n")

    for device_name, ip in devices.items():

        current_status = ping_device(ip)

        print(
            f"{device_name} is "
            f"{current_status['status']} "
            f"({current_status['response_time']} ms)"
        )

        # Check if status changed
        if device_name in previous_status:

            if previous_status[device_name]['status'] != current_status['status']:

                print(
                    f"ALERT: {device_name} changed from "
                    f"{previous_status[device_name]['status']} "
                    f"to {current_status['status']}"
                )

                # Save alert to log file
                with open("src/network_logs.txt", "a") as log_file:

                    log_file.write(
                        f"{datetime.now()} - "
                        f"{device_name} changed from "
                        f"{previous_status[device_name]['status']} to "
                        f"{current_status['status']}\n"
                    )

        # Update status
        previous_status[device_name] = current_status

    print("\nChecking again in 5 seconds...\n")

    time.sleep(5)