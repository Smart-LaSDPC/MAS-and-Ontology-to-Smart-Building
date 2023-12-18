import paho.mqtt.client as mqtt
import time
import json
import sys

broker = '192.168.1.157'
port = 1883
#client_id = 'DevicesInLab'
topicDevices = 'UpdateState'
publishTopic = 'DevicesStates'

device_config=dict()
device_config["state"] = "OFF"

client_id = "Devices"

state = {}
state["Bulb_1"] = "ON"
state["AirConditioner_1"] = "OFF"
state["Door_1"] = "OPEN"
state["Window_1"] = "CLOSED"

Bulb = {}
Bulb["Bulb_1"] = None

AirCond = {}
AirCond["AirConditioner_1"] = None

Door = {}
Door["Door_1"] = None

Window = {}
Window["Window_1"] = None

#client_id = sys.argv[1]

def on_connect(client, userdata, flags, rc):
	#print('connected (%s)' % client._client_id)
	client.subscribe(topic=topicDevices, qos=1)

def air_conditioning():
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y %H:%M:%S", named_tuple)

    for key in AirCond:
        air_message = ('{ "id":"'+str(key)+'",'
            +'"type":"air_conditioner",'
            +'"date":"'+str(time_string)+'",'
            +'"state":"'+str(state[str(key)])+'" }')
    
    return air_message

def bulb():
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y %H:%M:%S", named_tuple)

    for key in Bulb:
        bulb_message = ('{ "id":"'+str(key)+'",'
            +'"type":"bulb",'
            +'"date":"'+str(time_string)+'",'
            +'"state":"'+str(state[str(key)])+'" }')

    return bulb_message

def door():
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y %H:%M:%S", named_tuple)

    for key in Door:
            door_message = ('{ "id":"'+str(key)+'",'
                +'"type":"door",'
                +'"date":"'+str(time_string)+'",'
                +'"state":"'+str(state[str(key)])+'" }')
            
    return door_message

def window():
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y %H:%M:%S", named_tuple)

    for key in Window:
        window_message = ('{ "id":"'+str(key)+'",'
            +'"type":"window",'
            +'"date":"'+str(time_string)+'",'
            +'"state":"'+str(state[str(key)])+'" }')
    
    return window_message

def getMessageFromDevice():
    #PREPARING MESSAGE FOR DEVICE
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y %H:%M:%S", named_tuple)

    for key in AirCond:
        air_message = ('{ "id":"'+str(key)+'",'
            +'"type":"air_conditioner",'
            +'"date":"'+str(time_string)+'",'
            +'"state":"'+str(state[str(key)])+'" }')
    
    for key in Bulb:
        bulb_message = ('{ "id":'+str(key)+','
            +'"type":"bulb",'
            +'"date":"'+str(time_string)+'",'
            +'"state":"'+str(state[str(key)])+'" }')
    
    for key in Door:
        door_message = ('{ "id":'+str(key)+','
            +'"type":"door",'
            +'"date":"'+str(time_string)+'",'
            +'"state":"'+str(state[str(key)])+'" }')
        
    for key in Window:
        window_message = ('{ "id":'+str(key)+','
            +'"type":"window",'
            +'"date":"'+str(time_string)+'",'
            +'"state":"'+str(state[str(key)])+'" }')
    
    sensor_message = air_message + "\n"\
                     + bulb_message + "\n"\
                     + door_message + "\n"\
                     + window_message + "\n"
    
    return sensor_message

def upadateState(id, status):
    if status != state[id]:
        print("\n=============================================================")
        print(">>>> Updating the state of " + id + ": " + state[id]+" --> "+status)
        print("=============================================================")
        state[id] = status

def publish(client, payload):
    client.publish(publishTopic, payload, 0, True)
    print(payload)

def publish_status_messages(client):
    print("\n------------------------------ Publishing ------------------------------\n")
    client.payload = air_conditioning()
    publish(client, client.payload)

    client.payload = bulb()
    publish(client, client.payload)

    client.payload = door()
    publish(client, client.payload)

    client.payload = window()
    publish(client, client.payload)

def on_message(client, userdata, message):
    messageReceived = message.payload.decode("utf-8")
    data = json.loads(messageReceived)
    status = data["state"]
    id = data["id"]
    upadateState(id, status)



client = mqtt.Client(client_id, clean_session=True)
client.on_connect = on_connect
client.on_message = on_message
client.connect(host='127.0.0.1', port=1883)


try:
    client.loop_start()
    while True:
        time.sleep(1)
        publish_status_messages(client)
except KeyboardInterrupt:
    print("Closing the connection")
    client.loop_stop()
    client.disconnect()
    sys.exit(0)

