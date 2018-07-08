# ************************************************************
# Copyright (c) 2017 IBM Corporation and other Contributors.
#
# Modified by Luan H Alves
# Date: 24/03/2018
# ************************************************************

import sys
import datetime
import ibmiotf.gateway
from time import sleep
from random import uniform, randint
from ibmiotf.codecs import jsonCodec


org = "n3e46k"
gatewayType = "gateway_test"
gatewayId = "raspberry"
authMethod = "token"
authToken = "M5d@)YoQqAU)C-e?MZ"


def publish_callback():
    print("Mensagem recebida por IBM Watson IoT Platform")


def timestamp():
    str_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    return str_time


try:
    gatewayCred = {"org": org, "type": gatewayType, "id": gatewayId, "auth-method": authMethod, "auth-token": authToken}
    gatewayCli = ibmiotf.gateway.Client(gatewayCred)
except Exception as e:
    print("[Exc01] exception connecting device: %s" % str(e))
    sys.exit()


gatewayCli.connect()

for i in range(0, 20):

    try:
        # DADOS SIMULADOS PARA OS TESTES
        sensorValues = {
                        "state": "true",
                        "gateway": 1,
                        "node": randint(1, 10),
                        "timestamp": timestamp(),
                        "QY": round(uniform(0.6, 0.7), 4),
                        "temperature": round(uniform(17.0, 18.0), 1),
                        "latitude": (-19.883971),
                        "longitude": (-44.415545)
                       }

        state = sensorValues["state"]
        gateway = sensorValues["gateway"]
        node = sensorValues["node"]
        date = sensorValues["timestamp"]
        qy = sensorValues["QY"]
        temperature = sensorValues["temperature"]
        latitude = sensorValues["latitude"]
        longitude = sensorValues["longitude"]

        payload = {
                    "gateway"+str(gateway): {
                        "node"+str(node): {
                            "state": state,
                            "timestamp": date,
                            "QY": qy,
                            "temperature": temperature,
                            "latitude": latitude,
                            "longitude": longitude
                        }
                    }
        }

        gatewayCli.setMessageEncoderModule("json", jsonCodec)

        gatewaySuccess = gatewayCli.publishGatewayEvent("sensor-events", "json", payload, qos=2, on_publish=publish_callback)
        print('\n' + str(payload) + '\n')

        if not gatewaySuccess:
            print("Gateway nao esta conectado ao IBM Watson IoT Platform.")

        sleep(3)

    except Exception as e:
        gatewayCli.disconnect()
        print("[Exc02] Gateway desconectado. %s" % str(e))

gatewayCli.disconnect()
