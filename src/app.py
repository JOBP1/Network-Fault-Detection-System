from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Devices to monitor
devices = [
    "127.0.0.1",
    "8.8.8.8",
    "10.255.255.1"
]

def ping_device(ip):
    response = os.system(f"ping -c 1 {ip} > /dev/null 2>&1")

    if response == 0:
        return "ONLINE"
    else:
        return "OFFLINE"

@app.route("/")
def dashboard():

    device_status = {}

    for device in devices:
        device_status[device] = ping_device(device)

    html = """
    <html>
    <head>
        <title>Network Monitoring Dashboard</title>
    </head>
    <body>
        <h1>Network Monitoring Dashboard</h1>

        <table border="1" cellpadding="10">
            <tr>
                <th>Device IP</th>
                <th>Status</th>
            </tr>

            {% for device, status in device_status.items() %}
            <tr>
                <td>{{ device }}</td>
                <td>{{ status }}</td>
            </tr>
            {% endfor %}
        </table>

    </body>
    </html>
    """

    return render_template_string(html, device_status=device_status)

if __name__ == "__main__":
    app.run(debug=True)