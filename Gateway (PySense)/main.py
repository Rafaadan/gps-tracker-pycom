###############################################################################
#               MÁSTER EN INGENIERÍA DE TELECOMUNICACIÓN                      #
# Autores: Rafael Adán López y David Fernández Martínez                       #
# Fecha: 17 de enero de 2023                                                  #
#                                                                             #
###############################################################################

#IImport libraries
import config
from nanogateway import NanoGateway

#Create the nanogateway object 
if __name__ == '__main__':
    nanogw = NanoGateway(
        id=config.GATEWAY_ID,
        frequency=config.LORA_FREQUENCY,
        datarate=config.LORA_GW_DR,
        ssid=config.WIFI_SSID,
        password=config.WIFI_PASS,
        server=config.SERVER,
        port=config.PORT,
        ntp_server=config.NTP,
        ntp_period=config.NTP_PERIOD_S
        )

    nanogw.start()
    #nanogw._log('You may now press ENTER to enter the REPL')
    input()

    