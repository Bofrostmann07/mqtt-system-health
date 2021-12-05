# -- coding: utf-8 --
import psutil
import json
# import context  # Ensures paho-mqtt is in Python path
import paho.mqtt.publish as publish
import platform
import time
import datetime

raw_general = platform.uname()
processor_type = platform.processor()

raw_memory = psutil.virtual_memory()
raw_cpu = psutil.cpu_percent(interval=1)
raw_disk = psutil.disk_usage('/')

cpu_utilization = raw_cpu

memory_total = round(raw_memory.total * 0.000000001, 2)
memory_free = round(raw_memory.available * 0.000000001, 2)
memory_used = round(raw_memory.used * 0.000000001, 2)
memory_used_percent = raw_memory.percent

disk_total = round(raw_disk.total * 0.000000001, 2)
disk_free = round(raw_disk.free * 0.000000001, 2)
disk_used = round(raw_disk.used * 0.000000001, 2)
disk_used_percent = raw_disk.percent

timestamp = round(time.time(), 0)
# Compliant with RFC3339 and ISO 8601
date = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%SZ")

message = {
    "general": {
        "hostname": raw_general.node,
        "system": raw_general.system,
        "release": raw_general.release,
        "version": raw_general.version,
        "machine": raw_general.machine,
        "processor": processor_type
    },
    "cpu": {
        "utilization": cpu_utilization
    },
    "memory": {
        "total": memory_total,
        "free": memory_free,
        "used": memory_used,
        "used_percent": memory_used_percent
    },
    "disk": {
        "total": disk_total,
        "free": disk_free,
        "used": disk_used,
        "used_percent": disk_used_percent
    },
    "network": {
    },
    "time": timestamp,
    "date": date
}

raw_network = psutil.net_if_stats()
network = {}
for x in raw_network:
    for y in raw_network.values():
        data = {
            x: {
                "interface": x,
                "status": y.isup,
                "duplex": y.duplex,
                "speed": y.speed,
                "mtu": y.mtu
            }
        }
        network.update(data)
message["network"].update(network)

# print(message["network"])

system_health = json.dumps(message)
mqtt_topic = "system_health/info/" + raw_general.node
publish.single(mqtt_topic, system_health, hostname="10.30.0.3")
