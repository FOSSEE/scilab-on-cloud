#!/bin/bash

# Start

export WORKING_DIR="/scilab-on-cloud"
export SOC_PID="/tmp/scilab.on.cloud.pid"

#Start

start()
{
    screen -dmS screencloud sh -c "cd $WORKING_DIR ; source /opt/rh/rh-python36/enable  ; source /soc_env/bin/activate ; nohup $WORKING_DIR/run.sh"
}

# Stop

stop()
{
    kill -15 $(cat $SOC_PID)
    sleep 30
    screen -X -S screencloud quit


}

case "$1" in
    start)
        stop
        start
        ;;
     stop)
        stop
        ;;
        *)
        echo "cloud.start.stop.sh {start|stop}"
        exit 1
        ;;
esac
exit $?
