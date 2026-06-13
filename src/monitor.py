import os
import subprocess
import paramiko
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

def ssh_check():
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(
                hostname="192.168.30.3",
                username="ubuntu",
                password="ubuntu"
            )

            stdin, stdout, stderr = ssh.exec_command("free -m | grep Mem:")
            cpu_stdin, cpu_stdnout, cpu_stderr = ssh.exec_command("top -bn1 | grep '%Cpu'")
            cpu_output = cpu_stdnout.read().decode().strip()
            print("CPU OUTPUT:", cpu_output)
            output = stdout.read().decode().strip().split()
            cpu_parts =cpu_output.split(",")
            cpu_idle = cpu_parts[3].strip().split(" ")[0]
            cpu_usage = round(100 - float(cpu_idle), 1)

            print(output)

            total_memory = output[1]
            used_memory = output[2]
            free_memory = output[3]
            
            return {
                "ssh_status": "CONNECTED",
                "total_memory": total_memory,
                "used_memory": used_memory,
                "free_memory": free_memory,
                "cpu_usage": cpu_usage
            }

        except Exception as e:
            print("SSH ERROR:", e)

            return {
                "ssh_status": "FAILED",
                "memory_data": str(e)
            }

ssh_result = ssh_check()

print(ssh_result["ssh_status"])
print("Used:", ssh_result["used_memory"])
print("Free:", ssh_result["free_memory"])

if __name__ == "__main__":
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
