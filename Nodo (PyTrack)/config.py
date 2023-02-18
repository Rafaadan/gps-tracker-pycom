###############################################################################
#               MÁSTER EN INGENIERÍA DE TELECOMUNICACIÓN                      #
# Autores: Rafael Adán López y David Fernández Martínez                       #
# Fecha: 17 de enero de 2023                                                  #
#                                                                             #
###############################################################################

""" LoPy LoRaWAN Nano Gateway configuration options """

import machine
import ubinascii

WIFI_MAC = ubinascii.hexlify(machine.unique_id()).upper()
# Set  the Gateway ID to be the first 3 bytes of MAC address + 'FFFE' + last 3 bytes of MAC address
GATEWAY_ID = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]

#SERVER = 'router.eu.thethings.network'
SERVER = 'eu1.cloud.thethings.network'

PORT = 1700

NTP = "pool.ntp.org"
NTP_PERIOD_S = 3600

#SSID and password of the WiFi
WIFI_SSID = 'GPS'
WIFI_PASS = 'GPS12345'

# for EU868
LORA_FREQUENCY = 868100000
LORA_GW_DR = "SF7BW125" # DR_5
LORA_NODE_DR = 5

