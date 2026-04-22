This folder contains system design diagrams such as architecture and flowcharts.
The system is designed to monitor network devices within a virtualized environment. Virtual machines act as simulated network devices such as clients and servers.
The monitoring module continously sends ping requests to these devices to check their availability and response times. The collected data is passed to the fault detection engine, which analyzes the responses to determine whether a device is functioning normally or has failed.
If a fault is detected, the alert module is triggered to send notifications to the network administrator. At the same time, all device statuses and detected faults are recorded and displayed through the dashboard and log storage system.
The system operates in a continuous loop to ensure real-time monitoring and quick detection of network issues.
