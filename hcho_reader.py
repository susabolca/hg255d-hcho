#!/usr/bin/env python

import config
import serial
import struct
import time
import os

# DART HCHO sensor
class HCHO:

    def __init__(self, com="COM3", bps=9600):
        self._serial = serial.Serial(com, bps, timeout=1)
        self.led = 0

    def Read(self):
        a = bytearray(self._serial.read(9))
        chksum = sum(a) & 0xFF
        if chksum != 0xFF:
            raise Exception('Checksum failed.', chksum)

        b = struct.unpack('>BBBBHHB', a)
        ppm = b[4]
        ppm_max = b[5]
        self.Led()
        return ppm, ppm_max

    def Led(self):
        os.system("echo %d > /sys/class/leds/hg255d\:green\:usb/brightness" % (self.led))
        self.led = not self.led 

def Loop():
    sensor = HCHO('/dev/ttyUSB0')
    
    while True:
        avg = 0.0
        sec = config.Interval
        for i in range(sec):
            ppm, limit = sensor.Read()
            avg += ppm
        avg /= sec

        print("hcho_ppm: %.1f" % avg)
        data = 'iot_sensor_hcho_ppm{max="%d"} %.1f' % (limit, avg)
        curl = 'curl --user %s:%s --data-binary @- %s' % (config.Username, config.Password, config.PushUrl)
        os.system("echo '%s' | %s" % (data, curl))

while True:
    try:
        Loop()
    except Exception as e:
        print(e)
        time.sleep(3)