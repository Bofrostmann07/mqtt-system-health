# -- coding: utf-8 --

import psutil
import json

raw_memory = psutil.virtual_memory()

memory_total = round(raw_memory.total * 0.000000001, 2)
memory_available = round(raw_memory.available * 0.000000001, 2)
memory_free = round(raw_memory.free * 0.000000001, 2)

message = {
  "cpu": {
    "total": memory_total,
    "available": memory_available,
    "free": memory_free,
  }
}

system_health = json.dumps(message)

print(system_health)
