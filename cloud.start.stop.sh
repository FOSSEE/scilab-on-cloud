#!/bin/bash

# Start

export WORKING_DIR="PATH_to_CLOUD_DIR"
#SOC_PID=$WORKING_DIR"/scilab.on.cloud.pid"
export SOC_PID="PATH_to_CLOUD_DIR/tmp/scilab.on.cloud.pid"


start()
{
 
    #su - scilab.cloud
    #cd $WORKING_DIR
    #. ../env_cloud/bin/activate
    screen -dmS myscilabcloud sh -c "cd $WORKING_DIR ; source PATH_to_python/rh-python36/enable  ; source PATH_to_CLOUD_DIR/scilab-on-cloud_env/bin/activate ; nohup $WORKING_DIR/run.sh"
    #echo $(ps -eo comm,pid,etimes | awk '/^scilab-adv-cli/ { $1=""; print $0 }') > /run/scilab.on.cloud.pid
    #sleep 10
    #echo $(ps -eo comm,pid,etimes | awk '/^scilab-bin/ { print $2 }') > $SOC_PID
}

# Stop

stop()
{
    kill -15 $(cat $SOC_PID)
    sleep 30
    screen -X -S myscilabcloud quit
    #rm -fr $SOC_PID

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
