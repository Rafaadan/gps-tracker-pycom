#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

from network import LoRa
import socket
import binascii
import struct
import time
import config

#Imports gps
import machine
import math
import network
import os
import utime
import gc
from machine import RTC
from machine import SD
from L76GNSS import L76GNSS
from pycoproc_1 import Pycoproc

from network import LoRa
import socket
import time

time.sleep(2)
gc.enable()

# setup rtc
rtc = machine.RTC()
rtc.ntp_sync("pool.ntp.org")
utime.sleep_ms(750)
print('\nRTC Set from NTP to UTC:', rtc.now())
utime.timezone(7200)
print('Adjusted from UTC to EST timezone', utime.localtime(), '\n')

py = Pycoproc(Pycoproc.PYTRACK)
l76 = L76GNSS(py, timeout=30)

pybytes_enabled = False
if 'pybytes' in globals():
    if(pybytes.isconnected()):
        print('Pybytes is connected, sending signals to Pybytes')
        pybytes_enabled = True


# initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify('260B938E'))[0]
nwk_swkey = binascii.unhexlify('84128363EE0F750D9B9722CACC7D1745')
app_swkey = binascii.unhexlify('77F0E84DF19B567C76AE6D13E5CE15A3')

# remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)

# set the 3 default channels to the same frequency
lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)

# make the socket non-blocking
s.setblocking(False)

while True:
    coord = l76.coordinates()
    #f.write("{} - {}\n".format(coord, rtc.now()))
    print("{} - {} - {}".format(coord, rtc.now(), gc.mem_free()))
    if(pybytes_enabled):
        pybytes.send_signal(1, coord)
    if coord != (None, None):
        pkt = '{},{}'.format(coord[0],coord[1])
        print(pkt)
        s.send(pkt)
    else:
        print("GPS con mal rendimiento bro")
    print("Durmiendo 5s")
    time.sleep(5)

    #pkt = b'PKT #' + bytes([i])
    #print('Sending:', pkt)
    #s.send(pkt)
    #time.sleep(4)
    #rx, port = s.recvfrom(256)
    #if rx:
    #    print('Received: {}, on port: {}'.format(rx, port))
    #time.sleep(6)