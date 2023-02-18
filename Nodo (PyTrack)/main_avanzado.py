###############################################################################
#               MÁSTER EN INGENIERÍA DE TELECOMUNICACIÓN                      #
# Autores: Rafael Adán López y David Fernández Martínez                       #
# Fecha: 17 de enero de 2023                                                  #
#                                                                             #
###############################################################################

#Import libraries
import socket
import binascii
import struct
import time
import config
import math
import machine
from network import LoRa
from machine import Pin
import os
import utime
import gc
from L76GNSS import L76GNSS
from pycoproc_1 import Pycoproc
from LIS2HH12 import LIS2HH12

#Mean filter of 5 length with lattitude and longitude
tam = 5
buffer_lat = [0, 0, 0, 0, 0]
buffer_lon = [0, 0, 0, 0, 0]

def mean(data):
    return sum(data)/len(data)

def my_interrupt_handler(source):

    """
    Function that will be called when there is an interruption due to the acelerometer. When it is called, 
    it will send via LoraWan the following data:
    {latitude, longitude, name, battery}

    """
    global tam
    global buffer_lat
    global buffer_lon
    
    #Data adquisition
    name = "Animal"
    battery = py.read_battery_voltage()
    coord = l76.coordinates()

    #Sending via PyBytes if it is enabled (discomment only if you have access to WiFi)
    if(pybytes_enabled):
        pybytes.send_signal(1, coord)

    #It will only send data if the GPS get data
    if coord !=(None,None):
        print("Nueva coord: {}".format(coord))
        # Meter muestra de latitud en el buffer
        buffer_lat=buffer_lat[1:tam-1]
        buffer_lat.append(coord[0])

        # Meter muestra de longitud en el buffer
        buffer_lon=buffer_lon[1:tam-1]
        buffer_lon.append(coord[1])

        # Se calcula el valor medio
        latitud_media=mean(buffer_lat)
        longitud_media=mean(buffer_lon)

        if(pybytes_enabled):
            pybytes.send_signal(1, coord)

        pkt = '{},{},{},{}'.format(latitud_media,longitud_media,nombre,bateria)
        print(pkt)
        try:
            s.send(pkt)
        except:
            print("Error de memoria")
    else:
        print("No signal")
    gc.collect()
    
#Memory management
gc.enable()

#Creating neccesary objects
py = Pycoproc(Pycoproc.PYTRACK) #PyTrack 2.0X
l76 = L76GNSS(py, timeout=30) #GPS module
accel = LIS2HH12() #Accelerometer

#Checking the conexion with PyBytes as specified in pybytes_config.json (discomment only if you have Wifi access)
global pybytes_enabled
pybytes_enabled = False

if 'pybytes' in globals():
    if(pybytes.isconnected()):
        print('Pybytes is connected, sending signals to Pybytes')
        pybytes_enabled = True


#Inicialize Lora network
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# Crate ABP parameters
dev_addr = struct.unpack(">l", binascii.unhexlify('260B938E'))[0]
nwk_swkey = binascii.unhexlify('84128363EE0F750D9B9722CACC7D1745')
app_swkey = binascii.unhexlify('77F0E84DF19B567C76AE6D13E5CE15A3')

# Delete unused channels
for i in range(3, 16):
    lora.remove_channel(i)

#Setting default channels
lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

#Joining ABP network (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

#Creating Lora socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Adjusting data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)
s.setblocking(False)

#Loop wating for the GPS module to reach signal
coord = (None, None)
while coord == (None, None):
    print("No signal")
    coord = l76.coordinates()

#Sending via PyBytes if it is enabled (discomment only if you have access to WiFi)
#if(pybytes_enabled):
#    pybytes.send_signal(1, coord)


name="Vaca"
for i in range(0,tam):
    coord=l76.coordinates()
    buffer_lat[i]=coord[0]
    buffer_lon[i]=coord[1]
    battery = py.read_battery_voltage()
    pkt = '{},{},{},{}'.format(coord[0],coord[1],name,battery)

#Interruption of the acelerometer
accel.enable_activity_interrupt(400,200,my_interrupt_handler)

while(True):
    pass