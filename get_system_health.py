# -- coding: utf-8 --
#
# To-Do: Temperaturen und Lüftergeschwindigkeit auslesen
#
#
#

import psutil
import json
#import context  # Ensures paho-mqtt is in PYTHONPATH
import paho.mqtt.publish as publish
import platform


hostname = platform.node()
system_name = platform.system()
machine_name = platform.machine()
processor_type = platform.processor()

raw_memory = psutil.virtual_memory()
raw_cpu = psutil.cpu_percent(interval=1)
raw_disk = psutil.disk_usage('/')

cpu_utilization = raw_cpu

memory_total = round(raw_memory.total * 0.000000001, 2)
memory_free = round(raw_memory.free * 0.000000001, 2)
memory_used = round(raw_memory.used * 0.000000001, 2)
memory_used_percent = raw_memory.percent

disk_total = round(raw_disk.total * 0.000000001, 2)
disk_free = round(raw_disk.free * 0.000000001, 2)
disk_used = round(raw_disk.used * 0.000000001, 2)
disk_used_percent = raw_disk.percent

message = {
  "general": {
   "hostname": hostname,
   "system": system_name,
   "machine": machine_name,
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
  }
}

system_health = json.dumps(message)
mqtt_topic = "system_health/" + hostname
publish.single(mqtt_topic, system_health, hostname="10.30.0.3")

#print(test)
