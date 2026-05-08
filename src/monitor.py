import os
import time

def ping_device(ip):
    response = os.system(f"ping -c 1 {ip} > /dev/null 2>&1")

    if response == 0:
        return "ONLINE"
    else:
        return "OFFLINE"

# Devices to monitor
devices = [
    "127.0.0.1",
    "8.8.8.8",
    "10.255.255.1"
]

# Store previous statuses
previous_status = {}

while True:
    print("\n--- Network Monitoring ---\n")

    for device in devices:
        current_status = ping_device(device)

        print(f"{device} is {current_status}")

        # Check if status changed
        if device in previous_status:
            if previous_status[device] != current_status:
                print(f"ALERT: {device} changed from {previous_status[device]} to {current_status}")

        # Update status
        previous_status[device] = current_status

    print("\nChecking again in 5 seconds...\n")

    time.sleep(5)
