#!/usr/bin/python

from Adafruit_7Segment import SevenSegment
import spidev
import time
import os
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)
spi = spidev.SpiDev()
spi.open(0,0)
segment = SevenSegment(address=0x70)
DEBUG=1
print "Press CTRL+Z to exit"

def readadc(adcnum):
    if (adcnum > 7) or (adcnum < 0):
        return -1
    r = spi.xfer2([1,(8+adcnum)<<4,0])
    adcout = ((r[1]&3) << 8) + r[2]
    return adcout
# Light Sensor connected to adc #0
temp_adc = 4

# Continually update the time on a 4 char, 7-segment display
while True:
    GPIO.output(25, True)
    read_adc4 =readadc(temp_adc)

    millivolts = read_adc4 * ( 3300.0 / 1024.0)

    # 10 mv per degree
    temp_C = ((millivolts - 100.0) / 10.0) - 40.0

    # convert celsius to fahrenheit
    temp_F = ( temp_C * 9.0 / 5.0 ) + 32

    # remove decimal point from millivolts
    millivolts = "%d" % millivolts

    # show only one decimal place for temprature and voltage readings
    print_temp = int(temp_C*10)
    temp_C = "%.1f" % temp_C
    temp_F = "%.1f" % temp_F


    if DEBUG:
        print "read_adc4:\t", read_adc4
        print "millivolts:\t", millivolts
        print "temp_C:\t\t", temp_C
        print "temp_F:\t\t", temp_F
        print

    segment.writeDigit(0, (print_temp%10000)/1000)
    segment.writeDigit(1, (print_temp%1000)/100)
    segment.writeDigit(3, (print_temp%100)/10,True)
    segment.writeDigit(4, print_temp%10)
    time.sleep(.25)
    GPIO.output(25,False)
    time.sleep(.75)