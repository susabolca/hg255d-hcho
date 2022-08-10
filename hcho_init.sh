#!/bin/sh /etc/rc.common

START=99
STOP=15

HCHO_D=/root/hcho

start() {
    python $HCHO_D/hcho_reader.py &
}

stop() {
    echo "not support."
}