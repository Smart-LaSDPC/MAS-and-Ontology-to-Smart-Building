from owlready2 import *
import paho.mqtt.client as mqtt
import json
import signal
import os

things = {}
thingsType = {}
sensorData = {}
devices = {}

tempSensors = []
lightInSensors = []
lightOutSensors = []
motionSensors = []

bulbs = []
airConds = []
doors = []
blinds = []

canReceive = True
ruleApplied = False
base = "Laboratory"
v = 1
countRound = 0

directory_path = os.path.dirname(os.path.abspath(__file__))
delete_file = "Laboratory_v"
files = os.listdir(directory_path)

for file in files:
    if file.startswith(delete_file) and \
        file.endswith(".rdf"):
        file_path = os.path.join(directory_path, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                #print(f"Deleted {file}")
        except Exception as e:
            print(f"Error deleting {file}: {str(e)}")


def print_round():
    global countRound
    countRound = countRound+1
    print("\n******************************  R O U N D    "+str(countRound)+ \
          "  ******************************\n")

def handle_exit(signal, frame):
    if client.is_connected():
        client.disconnect()
    print("\nClosing the connection")
    sys.exit(0)

# =================  Connection to MQTT Broker ==================== #
broker = '192.168.1.157'
port = 1883
client_id = 'ReasonerAgent'
publish_topic = 'UpdateState'

def publish_update(client, payload):
    client.publish(publish_topic, payload, 0, False)

def has_all_sensors():
    return ("temperature" in sensorData and 
            "light_in" in sensorData and 
            "light_out" in sensorData and
            "motion" in sensorData)

def has_all_things():
    return ("air_conditioner" in thingsType and 
            "bulb" in thingsType and 
            "door" in thingsType and
            "blind" in thingsType)

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic='DevicesStates', qos=1)
    client.subscribe(topic='JsonData', qos=1)


def print_things():
    print("\n------ STATUS OF THINGS ------\n")
    for key in things:
        print(str(things[key]))

def print_sensors():
    print("\n------ STATUS OF SENSORS ------\n")
    for key in sensorData:
        print(str(sensorData[key]))


def on_message(client, userdata, message):
    global canReceive

    if message.topic == "DevicesStates":
        messageReceive = message.payload.decode("utf-8")
        data = json.loads(messageReceive)
        id = data["id"]
        type = data["type"]
        things[id] = data
        thingsType[type] = id
        
    if canReceive and message.topic == "JsonData":
        messageReceive = message.payload.decode("utf-8")
        data = json.loads(messageReceive)
        type = data["type"]
        sensorData[type] = data

        if has_all_sensors() and has_all_things():
            print_round()
            canReceive = False
            print_things()
            print_sensors()
            onto = load_onto()
            apply_instances(onto)

            
# ================= Manipulating the Ontology ==================== #

def load_onto():
    global base
    # Load the local ontology
    onto_path.append(".")
    onto = get_ontology(base + ".rdf").load()
    
    return onto

def apply_instances(onto):

    global v
    global ruleApplied
    global canReceive

    for key in things.keys():
        jsonData = things[key]
        thingType = jsonData["type"]

        if thingType == "bulb":
            bulb_instance(onto, jsonData)
        elif thingType == "air_conditioner":
            air_cond_instance(onto, jsonData)
        elif thingType == "door":
            door_instance(onto, jsonData)
        elif thingType == "blind":
            window_instance(onto, jsonData)
        

    for key in sensorData.keys():
        sensorType = key
        jsonData = sensorData[key]

        if sensorType == "temperature":
            temperature_instance(onto, jsonData)
        elif sensorType == "light_in":
            light_in_instance(onto, jsonData)
        elif sensorType == "light_out":
            light_out_instance(onto, jsonData)    
        elif sensorType == "motion":
            motion_instance(onto, jsonData)
    
    apply_rules(onto)

    if not ruleApplied:
        print("\n# None of the rules were applied!")
        save_onto(onto)

    ruleApplied = False

    # End of the current round of Json, calling the next round
    sensorData.clear()
    things.clear()
    canReceive = True


def bulb_instance(onto, jsonData):
    bulbID = jsonData["id"]
    bulbState = jsonData["state"]
    bulb_1 = onto.Bulb(bulbID)
    bulb_1.bulbState = [bulbState]
    bulbs.append(bulb_1)
    
def air_cond_instance(onto, jsonData):
    airCondID = jsonData["id"]
    airCondState= jsonData["state"]
    airCond_1 = onto.Air_conditioner(airCondID)
    airCond_1.airCondState = [airCondState]
    airConds.append(airCond_1)


def door_instance(onto, jsonData):
    doorID = jsonData["id"]
    doorState = jsonData["state"]
    door_1 = onto.Door(doorID)
    door_1.doorState = [doorState]
    doors.append(door_1)

def window_instance(onto, jsonData):
    windowID = jsonData["id"]
    windowState = jsonData["state"]
    window_1 = onto.Window(windowID)
    window_1.windowState = [windowState]
    blinds.append(window_1)

def  temperature_instance(onto, jsonData):
    # Create the instances 
    tempSensorID = jsonData["id"]
    tempSensor = onto.Temperature_Sensor(tempSensorID)
    
    # Assign the propertie for the instance created
    tempValue = jsonData["temperature"]
    tempSensor.tempValue = [tempValue]
    tempState = jsonData["state"]
    tempSensor.tempSensorState = [tempState]
    tempSensors.append(tempSensor)

def  light_in_instance(onto, jsonData):
    # Create the instances 
    lightSensorID = jsonData["id"]
    lightSensor = onto.Light_Sensor(lightSensorID)

    # Assign the propertie for the instance created
    lightValue = jsonData["lux"]
    lightSensor.lightValue = [lightValue]
    lightState = jsonData["state"]
    lightSensor.lightSensorState = [lightState]
    lightInSensors.append(lightSensor)

def  light_out_instance(onto, jsonData):
    # Create the instances 
    lightSensorID = jsonData["id"]
    lightSensor = onto.Light_Sensor(lightSensorID)

    # Assign the propertie for the instance created
    lightValue = jsonData["lux"]
    lightSensor.lightValue = [lightValue]
    lightState = jsonData["state"]
    lightSensor.lightSensorState = [lightState]
    lightOutSensors.append(lightSensor)

def  motion_instance(onto, jsonData):
    # Create the instances 
    motionSensorID = jsonData["id"]
    motiontSensor = onto.Motion_Sensor(motionSensorID)

    # Assign the propertie for the instance created
    motionValue = jsonData["detecting"]
    motiontSensor.motionValue = [motionValue]
    motionState = jsonData["state"]
    motiontSensor.motionSensorState = [motionState]
    motionSensors.append(motiontSensor)

def apply_rules(onto):

    with onto:

        global ruleApplied

        # -- Rule 1 --
        #    Turn off the bulb if no one is in the lab.
        for motionSensor in motionSensors:
            for bulb in bulbs:
                if ("ON" in motionSensor.motionSensorState and
                    "ON" in bulb.bulbState and
                    0 in motionSensor.motionValue):

                    print("\n# Rule 1 activated: turning OFF the " + str(bulb.name))
                    ruleApplied = True
                    bulb.bulbState = ["OFF"]
                    save_onto(onto)
                    ontoUpdated = load_onto()
                    update_things_status(str(bulb.name), "OFF")
                    apply_rules(ontoUpdated)

        # -- Rule 2 --
        #    Turn on the air conditioner if the temperature is greater than 28° C 
        #    and if someone is in the lab.
        for airCond in airConds:
            for motionSensor in motionSensors:
                for tempSensor in tempSensors:
                    if ("OFF" in airCond.airCondState and
                        "ON" in motionSensor.motionSensorState and
                        1 in motionSensor.motionValue and
                        "ON" in tempSensor.tempSensorState and
                        tempSensor.tempValue[0] > 28):

                        print("\n# Rule 2 activated: turning ON the " + str(airCond.name))
                        ruleApplied = True
                        airCond.airCondState = ["ON"]
                        save_onto(onto)
                        ontoUpdated = load_onto()
                        update_things_status(str(airCond.name), "ON")
                        apply_rules(ontoUpdated)

        # -- Rule 3 --
        #    Close the door if the air conditioning is on.
        for airCond in airConds:
            for door in doors:
                if ("ON" in airCond.airCondState and
                    "OPEN" in door.doorState):

                    print("\n# Rule 3 activated: closing the " + str(door.name))
                    ruleApplied = True
                    door.doorState = ["CLOSED"]
                    save_onto(onto)
                    ontoUpdated = load_onto()
                    update_things_status(str(door.name), "CLOSED")
                    apply_rules(ontoUpdated)

        # -- Rule 4 --
        #    Open the window if someone is in the lab, if the bulb is off
        #    and if the lux is between 50 and 200
        for blind in blinds:
            for motionSensor in motionSensors:
                for bulb in bulbs:
                    for lightInSensor in lightInSensors:
                        for lightOuSensor in lightOutSensors:
                            if ("CLOSED" in blind.windowState and
                                "ON" in motionSensor.motionSensorState and
                                1 in motionSensor.motionValue and
                                "OFF" in bulb.bulbState and
                                "ON" in lightInSensor.lightSensorState and
                                lightInSensor.lightValue[0] <= 200 and
                                lightOuSensor.lightValue[0] >= 300):
                                
                                print("\n# Rule 4 activated: opening the " + str(blind.name))
                                ruleApplied = True
                                blind.windowState = ["OPEN"]
                                save_onto(onto)
                                ontoUpdated = load_onto()
                                update_things_status(str(blind.name), "OPEN")


def update_things_status(id, new_status):
    data = things.get(id)
    if data:
        data["state"] = new_status
        publish_update(client, json.dumps(data))

def save_onto(onto):
    global v
    v = v+1
    lastVersion = base+"_v"+str(v)+".rdf"
    onto.save(file = lastVersion, format = "rdfxml")
            

signal.signal(signal.SIGINT, handle_exit)

client = mqtt.Client(client_id, clean_session=True)
client.on_connect = on_connect
client.on_message = on_message
client.connect(host='127.0.0.1', port=1883)
client.loop_forever()