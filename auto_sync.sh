#!/bin/bash

if [ "$1" = "start" ]; then
    LOG_LEVEL=DEBUG auto_sync -c config/sync_config.yml -l logs/auto_sync.log &
    echo $! > auto_sync.pid
elif [ "$1" = "stop" ]; then
    if [ -f auto_sync.pid ]; then
        kill $(cat auto_sync.pid)
        rm auto_sync.pid
    else
        echo "No PID file found. Is the process running?"
    fi
else
    echo "Usage: $0 {start|stop}"
fi
