#! /bin/bash

# nohup python3 export_container_count.py >/dev/null 2>&1 &
# Debugging!
nohup python3 -u export_container_count.py >nohup.out &

echo "Testing: curl localhost:8001/metrics"
