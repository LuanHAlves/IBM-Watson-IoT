# ************************************************************
# Copyright (c) 2017 IBM Corporation and other Contributors.
# Modified by Luan H Alves
# Date: 24/03/2018
# ************************************************************
import datetime
import signal
from time import sleep
import sys
import ibmiotf.gateway


def interruptHandler(signal, frame):
    gatewayCli.disconnect()
    sys.exit(0)


def myGatewayCommandCallback(command):
    print("Id = %s (of type = %s) received the gateway command %s at %s" % (
    command.id, command.type, command.data, command.timestamp))


def myDeviceCommandCallback(command):
    print("Id = %s (of type = %s) received the device command %s at %s" % (
    command.id, command.type, command.data, command.timestamp))


def myGatewayNotificationCallback(command):
    print("Id = %s (of type = %s) received the notification message %s at %s" % (
    command.id, command.type, command.data, command.timestamp))



signal.signal(signal.SIGINT, interruptHandler)
organization = "n3e46k"
gatewayType = "gateway_test"
gatewayId = "raspberry"
authMethod = "token"
authToken = "M5d@)YoQqAU)C-e?MZ"

print("Waiting for commands...")
# Initialize the device client.
try:
    gatewayOptions = {"org": organization, "type": gatewayType, "id": gatewayId,
                      "auth-method": authMethod, "auth-token": authToken}
    gatewayCli = ibmiotf.gateway.Client(gatewayOptions)
except Exception as e:
    print("Caught exception connecting device: %s" % str(e))
    sys.exit()

gatewayCli.connect()
print("After connect....")
print(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))


gatewayCli.subscribeToGatewayCommands(command='greeting', format='json', qos=2)
gatewayCli.commandCallback = myGatewayCommandCallback

gatewayCli.subscribeToGatewayNotifications()
gatewayCli.notificationCallback = myGatewayNotificationCallback


while True:

    try:
        sleep(1)
    except KeyboardInterrupt:
        gatewayCli.disconnect()
        print("\nDisconnected\n")
        sys.exit()