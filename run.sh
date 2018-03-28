#!/bin/sh

ext=".txt"
current_time=$(date +"%Y-%m-%d_%H:%M:%S")
file_name=$current_time$ext

echo "start processing"
python3 target_one.py > output/$file_name
echo "output/$file_name is ready"
