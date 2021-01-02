#!/bin/sh

while true; do
    level=$(echo get battery | nc -q 1 127.0.0.1 8423)
    now=$(date '+%Y-%m-%d %H:%M:%S')
    echo $now $level >> records.log
    sleep 5
done