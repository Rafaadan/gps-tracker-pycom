###############################################################################
#               MÁSTER EN INGENIERÍA DE TELECOMUNICACIÓN                      #
# Autores: Rafael Adán López y David Fernández Martínez                       #
# Fecha: 17 de enero de 2023                                                  #
#                                                                             #
###############################################################################

#Import libraries
from network import LoRa
import socket
import binascii
import struct
import time
import config
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

#Function that return the mean of a list
def mean(data):
    return sum(data)/len(data)

#Creating neccesary objects
py = Pycoproc(Pycoproc.PYTRACK)
l76 = L76GNSS(py, timeout=30)

pybytes_enabled = False
if 'pybytes' in globals():
    if(pybytes.isconnected()):
        print('Pybytes is connected, sending signals to Pybytes')
        pybytes_enabled = True


# initialize LoRa in LORAWAN mode.
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

#Mean filter of 10 length with lattitude and longitude
tam=10
global buffer_lat
global buffer_lon
buffer_lat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
buffer_lon = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#Initialize for the loop
coord=(None,None)

while coord==(None,None):
    coord=l76.coordinates()


if(pybytes_enabled):
    pybytes.send_signal(1, coord)

name="Vaca"
for i in range(0,tam-1):
    coord=l76.coordinates()
    buffer_lat[i]=coord[0]
    buffer_lon[i]=coord[1]
    battery = py.read_battery_voltage()
    pkt = '{},{},{},{}'.format(coord[0],coord[1],name,battery)
    try:
        s.send(pkt)
    except:
        print("Memory Error")

while True:
    inicio=time.time()
    name = "Vaca"
    battery = py.read_battery_voltage()
    coord = l76.coordinates()
    if coord !=(None,None):

        buffer_lat=buffer_lat[1:tam-1]
        buffer_lat.append(coord[0])

        buffer_lon=buffer_lon[1:tam-1]
        buffer_lon.append(coord[1])

        latitud_media=mean(buffer_lat)
        longitud_media=mean(buffer_lon)

        if(pybytes_enabled):
            pybytes.send_signal(1, coord)

        pkt = '{},{},{},{}'.format(latitud_media,longitud_media,name,battery)
        print(pkt)
        try:
            s.send(pkt)
        except:
            print("Memory Error")
        
    else:
        print("No signal")
    
    final=time.time()
    print("Tiempo={}".format(final-inicio))

    time.sleep(1)

