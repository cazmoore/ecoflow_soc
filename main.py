import config
import requests
from twilio.rest import Client
from datetime import datetime

ef_endpoint = "https://iot1.ecoflow.com/api/v1/devices/queryDeviceData"

device_list = config.ef_devices.items()
time_now = datetime.now()
time_now = time_now.strftime("%H:%M")

for device in device_list:
    name = device[0]
    serial_no = device[1]

    parameters = {
        "sn": serial_no,
        "appkey": config.api_key
    }

    response = requests.get(ef_endpoint, params=parameters)
    device_data = response.json()

    msgSent = False

    try:
        state_of_charge = device_data["data"]["data"]["socSum"]
        socFound = True
    except KeyError:
        socFound = False

    if socFound:
        # noinspection PyUnboundLocalVariable
        if not msgSent and state_of_charge <= 25:
            client = Client(config.account_sid, config.auth_token)

            message = client.messages.create(
                body=f"{name} battery level is {state_of_charge}% at {time_now}.",
                from_=config.from_num,
                to=config.to_num
            )

            print(message.status)
            msgSent = True
        elif not msgSent and state_of_charge == 100:
            client = Client(config.account_sid, config.auth_token)

            message = client.messages.create(
                body=f"{name} battery level is fully charged at {time_now}.",
                from_=config.from_num,
                to=config.to_num
            )

            print(message.status)
            msgSent = True
        elif 25 < state_of_charge < 100:
            msgSent = False
