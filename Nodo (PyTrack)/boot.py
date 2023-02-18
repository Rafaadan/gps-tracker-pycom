###############################################################################
#               MÁSTER EN INGENIERÍA DE TELECOMUNICACIÓN                      #
# Autores: Rafael Adán López y David Fernández Martínez                       #
# Fecha: 17 de enero de 2023                                                  #
#                                                                             #
###############################################################################

from machine import UART
import machine
import os

uart = UART(0, baudrate=115200)
os.dupterm(uart)

machine.main('main.py')