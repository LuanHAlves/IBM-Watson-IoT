import datetime
import ibmiotf.device
from time import sleep
from random import randint, uniform


def publish_callback():
    print("Confirmed event received by IBM Watson IoT Platform")


def timestamp():
    str_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    return str_time


org = "n3e46k"
deviceType = "device_test"
deviceId = "device01"
authMethod = "token"
authToken = "h8Exjf29sAuT72Q&1j"

deviceOptions = {"org": org, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
deviceCli = ibmiotf.device.Client(deviceOptions)


deviceCli.connect()
for x in range(0, 20):
    data = {
            "state": "true",
            "gateway": 1,
            "node": randint(1, 10),
            "timestamp": timestamp(),
            "QY": round(uniform(0.4, 0.8), 3),
            "temperature": round(uniform(17.0, 18.0), 1)
            }

    success = deviceCli.publishEvent("event", "json", data, qos=1, on_publish=publish_callback())

    if not success:
        print("Not connected to IoTF")

    sleep(3)

deviceCli.disconnect()
