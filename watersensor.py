#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Script is for connecting a PI with a IFTTT service
# Checking for Humity, snednign warning
# When water level is higher, escalation E-Mail is sent
# When E-Mail send once - no other is send till sensor get's dry
# https://maker.ifttt.com/trigger/WaterLevel/with/key/{{key}}
# https://maker.ifttt.com/trigger/HumityLevel/with/key/{{key}}

from config import * #Just to make sure to not expose the secret to github
import RPi.GPIO as GPIO
import time
import urllib.request

# Set some generic Strings
HUMITYSTRING = "https://maker.ifttt.com/trigger/HumityLevel/with/key/" + secret + "/?value1=" + sensor
WATERSTRING = "https://maker.ifttt.com/trigger/WaterLevel/with/key/" + secret + "/?value1=" + sensor

# Set some of the pin defintions
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

# reistor setup 
photo_ch = 0

#port init
def init():
    GPIO.setwarnings(False)
    #script cleanup
    GPIO.cleanup()
    #numbering system - board vs BCM 
    GPIO.setmode(GPIO.BCM)
    # set up the interface pins
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
     
#read SPI data from MCP3008
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    
    GPIO.output(cspin, True)
    # start clock spin
    GPIO.output(clockpin, False)
    # bring CS low
    GPIO.output(cspin, False)

    commandout = adcnum
    # start bit + single-ended bit
    commandout |= 0x18
    # we only need to send 5 bits here
    commandout <<= 3
    
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)

    adcount = 0
    
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcount <<= 1
        if (GPIO.input(misopin)):
            adcount |= 0x1

    GPIO.output(cspin, True)
    
    #print ("adcount: " + str(adcount) + "\n")
    
    # first bit is 'null' so drop it
    adcount >>= 1       
    return adcount

def main():
    # Set some booleans needed
    water_detected = False
    humity_detected = False
    init()
    time.sleep(1)
    print ("Detect water level in heating locker activated!\n")
    #print (secret)
    while True:
        adc_value = readadc(photo_ch, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #print ("adc_value: " + str(adc_value) + "\n")
        if adc_value == 0:
            print ("No water detected yet!\n")
            humity_detected = False
            water_detected = False
        elif adc_value > 0 and adc_value < 10:
            print ("Some humity detected! But no panic in range of detection error!\n")
        elif adc_value >= 10 and adc_value < 30:
            print ("Some humity detected! But no panic yet!\n")
            if not humity_detected:
                urllib.request.urlopen(HUMITYSTRING).read()
                humity_detected = True
        elif adc_value >= 30 and adc_value < 200:
            print ("Looks like heavy water!\n")
            print ("The Waterlevel is: " + str("%.1f"%(adc_value/200.*100)) + "%\n")
            if not water_detected:
                urllib.request.urlopen(WATERSTRING).read()
                water_detected = True
        time.sleep(10)


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        pass
GPIO.cleanup()




