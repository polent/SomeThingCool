#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Script is for connecting a PI with a IFTTT service
# Checking for Humity, snednign warning
# When water level is higher, escalation E-Mail is sent
# When E-Mail send once - no other is send tilll sensor get's dry

import RPi.GPIO as GPIO
import time

#Set some of the pin defintions

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

# reistor setup 
photo_ch = 0

#port init
def init():
         GPIO.setwarnings(False)
         GPIO.cleanup()			#script cleanup
         GPIO.setmode(GPIO.BCM)		#numbering system - boeárd vs BCM 
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

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

def main():
         init()
         time.sleep(1)
         print ("detec water level in heating locker\n")
         while True:
              adc_value=readadc(photo_ch, SPICLK, SPIMOSI, SPIMISO, SPICS)
              if adc_value == 0:
                       print ("no water detected\n")
              elif adc_value>0 and adc_value<30 :
                       print ("some humity detected\n")
              elif adc_value>=30 and adc_value<200 :
                       print ("looks like heavy water")
                       print ("calculated level: "+str("%.1f"%(adc_value/200.*100))+"%\n")
              time.sleep(10)


if __name__ == '__main__':
         try:
                  main()
                 
         except KeyboardInterrupt:
                  pass
GPIO.cleanup()




