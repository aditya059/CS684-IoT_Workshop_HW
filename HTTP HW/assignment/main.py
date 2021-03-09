import time
from api import ServerApi

serverApiObject = ServerApi()
serverApiObject.login('kachraseth@cs684.edu', 'kachraseth')
id2 = ''

def first_use_case() -> None:
    """
    Complete the below steps
    1. Create 2 things, "Device1" and "Device2"
    2. Delete "Device1"
    3. Update name of "Device2" to "device-2"
    4. Loop 5 times
    4.1 Report random (arbitrary) values for temperature and humidity on "device-2"
    4.2 Add a delay of 1 second
    4.3 Listen for RPC commands if any.

    The default baseUrl to use is https://apihptu.e-yantra.org/api

    NOTE: Please use the username and password provided to you by e-Yantra team.
    Contact e-Yantra team if not received.
    """
    global id2
    # 1
    device1 = serverApiObject.create_thing('Device1')
    id1 = device1['id']
    device2 = serverApiObject.create_thing('Device2')
    id2 = device2['id']
    # 2
    serverApiObject.delete_thing(id1)
    # 3
    serverApiObject.update_thing(id2, name= 'device-2')
    # 4
    accessToken2 = serverApiObject.client_token(id2)
    for i in range(5):
        # 4.1
        serverApiObject.add_telemetry(accessToken2, data={'temperature': i * 10, 'humidity': i * 15})
        print('Telemetry: ', serverApiObject.get_thing_telemetry(id2, "2020-02-19 00:00:00", "2022-02-19 16:45:00"))
        # 4.2
        time.sleep(1)
        # 4.3
        serverApiObject.receive_rpc(accessToken2)


def second_use_case(thing_id) -> None:
    """
    Complete the below steps for a thing with id `thing_id`
    1. Get data between time '2017-10-30 09:00:00' to '2021-06-10 17:00:00'.
    Use ServerApi::get_thing_telemetry().
    2. Send RPC command:- method: 'setTap', params: True

    The default baseUrl to use is https://apihptu.e-yantra.org/api

    NOTE: Please use the username and password provided to you by e-Yantra team.
    Contact e-Yantra team if not received.
    """
    # 1
    serverApiObject.get_thing_telemetry(thing_id, '2017-10-30 09:00:00', '2021-06-10 17:00:00')
    # 2
    serverApiObject.send_rpc(thing_id, method= 'setTap', params= True)

if __name__ == "__main__":
    first_use_case()
    print("---------------------------------------")
    second_use_case(id2)  # you can enter your thing_id here