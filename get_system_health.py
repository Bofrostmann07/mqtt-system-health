# -- coding: utf-8 --
import psutil
import json
import paho.mqtt.publish as publish
import platform
import time
import datetime


def is_main():
    return __name__ == "__main__"


# Collect system data
def query_system_data():
    system_data = {}

    # Collect and format general information
    raw_general_data = platform.uname()
    processor_type = platform.processor()
    general_data = {
        "hostname": raw_general_data.node,
        "system": raw_general_data.system,
        "release": raw_general_data.release,
        "version": raw_general_data.version,
        "machine": raw_general_data.machine,
        "processor": processor_type
    }
    system_data["general"] = general_data

    # Collect and format CPU information
    raw_cpu_data = psutil.cpu_percent(interval=1)
    cpu_data = {
        "utilization": raw_cpu_data
    }
    system_data["cpu"] = cpu_data

    # Collect and format memory information
    raw_memory_data = psutil.virtual_memory()
    memory_total = round(raw_memory_data.total * 0.000000001, 2)
    memory_free = round(raw_memory_data.available * 0.000000001, 2)
    memory_used = round(raw_memory_data.used * 0.000000001, 2)
    memory_used_percent = raw_memory_data.percent
    memory_data = {
        "total": memory_total,
        "free": memory_free,
        "used": memory_used,
        "used_percent": memory_used_percent
    }
    system_data["memory"] = memory_data

    # Collect and format disk information
    raw_disk_data = psutil.disk_usage('/')
    disk_total = round(raw_disk_data.total * 0.000000001, 2)
    disk_free = round(raw_disk_data.free * 0.000000001, 2)
    disk_used = round(raw_disk_data.used * 0.000000001, 2)
    disk_used_percent = raw_disk_data.percent
    disk_data = {
        "total": disk_total,
        "free": disk_free,
        "used": disk_used,
        "used_percent": disk_used_percent
    }
    system_data["disk"] = disk_data

    # Collect and format network information
    raw_network = psutil.net_if_stats()
    network_stats = {}
    for if_name, raw_if_stats in raw_network.items():
        if_stats = {
            "interface": if_name,
            "status": raw_if_stats.isup,
            "duplex": raw_if_stats.duplex,
            "speed": raw_if_stats.speed,
            "mtu": raw_if_stats.mtu
        }
        network_stats[if_name] = if_stats
    system_data["network"] = network_stats

    # Set timestamp
    timestamp = round(time.time(), 0)
    # Compliant with RFC3339 and ISO 8601
    date = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%SZ")
    time_data = {
        "timestamp": timestamp,
        "date": date
    }
    system_data.update(time_data)
    return system_data


def publish_mqtt_message(system_data):
    system_health = json.dumps(system_data)
    mqtt_topic = "system_health/info/" + system_data.get("general", {}).get("hostname", "unknown")
    publish.single(mqtt_topic, system_health, hostname="10.30.0.3")


if is_main():
    system_data = query_system_data()
    publish_mqtt_message(system_data)
