from flask import Flask, render_template_string
import subprocess
from datetime import datetime

app = Flask(__name__)

# Store previous statuses
previous_device_status = {}

# Store alert message
alert_message = ""

# Devices to monitor
devices = {
    "Localhost": "127.0.0.1",
    "Google DNS": "8.8.8.8",
    "Ubuntu VM": "192.168.30.3",
    "Test Offline Device": "10.255.255.1"
}


# Ping function
def ping_device(ip):
    try:
        result = subprocess.check_output(
            ["ping", "-c", "1", ip],
            universal_newlines=True
        )

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


@app.route("/")
def dashboard():

    global previous_device_status
    global alert_message

    device_status = {}

    last_updated = datetime.now().strftime("%H:%M:%S")

    # Reset alert each refresh
    alert_message = ""

    # Check all devices
    for device_name, ip in devices.items():

        result = ping_device(ip)

        device_status[device_name] = {
            "ip": ip,
            "status": result["status"],
            "response_time": result["response_time"]
        }

        # Detect status changes
        if device_name in previous_device_status:

            old_status = previous_device_status[device_name]
            new_status = result["status"]

            if old_status != new_status:

                if new_status == "OFFLINE":
                    alert_message = f"🚨 ALERT: {device_name} went OFFLINE"

                else:
                    alert_message = f"✅ ALERT: {device_name} is back ONLINE"

        # Save current status
        previous_device_status[device_name] = result["status"]

    html = """
    <html>

    <head>

        <title>Network Monitoring Dashboard</title>

        <meta http-equiv="refresh" content="5">

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>

            body {
                font-family: Arial, sans-serif;
                background-color: #0f172a;
                color: white;
                padding: 30px;
            }

            h1 {
                text-align: center;
                margin-bottom: 15px;
                color: #38bdf8;
                font-size: 42px;
            }

            .last-updated {
                text-align: center;
                color: #d1d1d1;
                font-size: 18px;
                margin-bottom: 30px;
            }

            .summary-container {
                display: flex;
                gap: 20px;
                justify-content: center;
                margin-bottom: 35px;
            }

            .card {
                background: #1e293b;
                padding: 20px;
                border-radius: 15px;
                width: 180px;
                text-align: center;
                box-shadow: 0 0 15px rgba(0,0,0,0.4);
            }

            .card h2 {
                margin: 0;
                font-size: 18px;
                color: #94a3b8;
            }

            .card p {
                font-size: 34px;
                margin-top: 10px;
                font-weight: bold;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                background: rgba(255,255,255,0.08);
                border-radius: 15px;
                overflow: hidden;
            }

            th {
                padding: 18px;
                background: rgba(255,255,255,0.15);
                font-size: 20px;
            }

            td {
                padding: 18px;
                text-align: center;
                font-size: 18px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }

            .status-online {
                color: #4cff4c;
                font-weight: bold;
            }

            .status-offline {
                color: #ff4c4c;
                font-weight: bold;
            }

            .status-container {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 10px;
                white-space: nowrap;
            }

            .status-dot {
                width: 12px;
                height: 12px;
                border-radius: 50%;
            }

            .green {
                background: #4cff4c;
                box-shadow: 0 0 10px #4cff4c;
            }

            .red {
                background: #ff4c4c;
                box-shadow: 0 0 10px #ff4c4c;
            }

            .alert-box {
                background: rgba(255, 76, 76, 0.2);
                color: #ff4c4c;
                border: 1px solid #ff4c4c;
                padding: 15px;
                width: 60%;
                margin: 20px auto;
                text-align: center;
                border-radius: 12px;
                font-size: 20px;
                font-weight: bold;
                box-shadow: 0 0 15px rgba(255,76,76,0.5);
            }

            .chart-container {
                width: 40%;
                max-width: 500px;
                height: 220px;
                margin: 40px auto;
                background: rgba(255,255,255,0.08);
                padding: 20px;
                border-radius: 20px;
            }

        </style>

    </head>

    <body>

        {% if alert_message %}
        <script>
            alert("{{ alert_message }}");
        </script>
        {% endif %}

        <h1>Network Monitoring Dashboard</h1>

        {% if alert_message %}
        <div class="alert-box">
            {{ alert_message }}
        </div>
        {% endif %}

        <p class="last-updated">
            Last Updated: {{ last_updated }}
        </p>

        <div class="summary-container">

            <div class="card">
                <h2>Total Devices</h2>
                <p>{{ device_status|length }}</p>
            </div>

            <div class="card">
                <h2>Online</h2>
                <p>
                    {{
                    device_status.values()
                    | selectattr("status", "equalto", "ONLINE")
                    | list
                    | length
                    }}
                </p>
            </div>

            <div class="card">
                <h2>Offline</h2>
                <p>
                    {{
                    device_status.values()
                    | selectattr("status", "equalto", "OFFLINE")
                    | list
                    | length
                    }}
                </p>
            </div>

        </div>

        <table>

            <tr>
                <th>Device Name</th>
                <th>IP Address</th>
                <th>Status</th>
            </tr>

            {% for device, status in device_status.items() %}

            <tr>

                <td>{{ device }}</td>

                <td>{{ status["ip"] }}</td>

                {% if status["status"] == "ONLINE" %}

                <td class="status-online">

                    <div class="status-container">

                        <span class="status-dot green"></span>

                        <span>
                            {{ status["status"] }}
                            ({{ status["response_time"] }} ms)
                        </span>

                    </div>

                </td>

                {% else %}

                <td class="status-offline">

                    <div class="status-container">

                        <span class="status-dot red"></span>

                        <span>
                            {{ status["status"] }}
                            ({{ status["response_time"] }})
                        </span>

                    </div>

                </td>

                {% endif %}

            </tr>

            {% endfor %}

        </table>

        <div class="chart-container">

            <div style="height: 200px;">
                <canvas id="responseChart"></canvas>
            </div>
        </div>

        <script>

            const ctx = document.getElementById('responseChart');

            const responseChart = new Chart(ctx, {

                type: 'bar',

                data: {

                    labels: [

                        {% for device, status in device_status.items() %}
                            "{{ device }}",
                        {% endfor %}

                    ],

                    datasets: [{

                        label: 'Response Time (ms)',

                        data: [

                            {% for device, status in device_status.items() %}

                                {% if status["response_time"] != "N/A" %}
                                    {{ status["response_time"] }},
                                {% else %}
                                    0,
                                {% endif %}

                            {% endfor %}

                        ],

                        backgroundColor: [
                            '#00ffcc',
                            '#00ffcc',
                            '#ff4c4c'
                        ],

                        borderWidth: 1

                    }]

                },

                options: {

                    responsive: true,
                    maintainAspectRatio: false,

                    plugins: {
                        legend: {
                            labels: {
                                color: 'white'
                            }
                        }
                    },

                    scales: {

                        y: {
                            beginAtZero: true,

                            ticks: {
                                color: "white"
                            },

                            grid: {
                                color: "rgba(255,255,255,0.1)"
                            }
                        },

                        x: {

                            ticks: {
                                color: "white"
                            },

                            grid: {
                                color: "rgba(255,255,255,0.1)"
                            }

                        }

                    }

                }

            });

        </script>

    </body>

    </html>
    """

    return render_template_string(
        html,
        device_status=device_status,
        last_updated=last_updated,
        alert_message=alert_message
    )


if __name__ == "__main__":
    app.run(debug=True)