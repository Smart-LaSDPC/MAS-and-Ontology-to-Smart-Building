# Inference Rules Test

Below is an example of 4 rounds of testing the inference rules.

```
*********************************  R O U N D    1  **********************************

------ STATUS OF THINGS ------

{'id': 'AirConditioner_1', 'type': 'air_conditioner', 'date': '11/09/2023 16:12:58', 
'state': 'OFF'}
{'id': 'Bulb_1', 'type': 'bulb', 'date': '11/09/2023 16:12:58', 'state': 'ON'}
{'id': 'Door_1', 'type': 'door', 'date': '11/09/2023 16:12:58', 'state': 'OPEN'}
{'id': 'Blind_1', 'type': 'blind', 'date': '11/09/2023 16:12:58', 'state': 'CLOSED'}

------ STATUS OF SENSORS ------

{'date': '11/09/2023 16:12:59', 'agent_id': 'Monitoring Agent_4', 'id': 'LightOutSensor_1', 'state': 'ON', 'type': 'light_out', 'lux': 423}
{'date': '11/09/2023 16:12:59', 'agent_id': 'Monitoring Agent_3', 'detecting': 0, 'id': 'MotionSensor_1', 'state': 'ON', 'type': 'motion'}
{'date': '11/09/2023 16:12:58', 'agent_id': 'Monitoring Agent_2', 'id': 'LightInSensor_1', 'state': 'ON', 'type': 'light_in', 'lux': 320}
{'date': '11/09/2023 16:12:58', 'agent_id': 'Monitoring Agent_1', 'temperature': 29, 'id': 'TempSensor_1', 'state': 'ON', 'type': 'temperature'}

# Rule 1 activated: turning OFF the Bulb_1

*********************************   R O U N D    2  *********************************

------ STATUS OF THINGS ------
{'id': 'AirConditioner_1', 'type': 'air_conditioner', 'date': '11/09/2023 16:13:03', 'state': 'OFF'}
{'id': 'Bulb_1', 'type': 'bulb', 'date': '11/09/2023 16:13:03', 'state': 'OFF'}
{'id': 'Door_1', 'type': 'door', 'date': '11/09/2023 16:13:03', 'state': 'OPEN'}
{'id': 'Blind_1', 'type': 'blind', 'date': '11/09/2023 16:13:03', 'state': 'CLOSED'}

------ STATUS OF SENSORS ------
{'date': '11/09/2023 16:13:04', 'agent_id': 'Monitoring Agent_4', 'id': 'LightOutSensor_1', 'state': 'ON', 'type': 'light_out', 'lux': 402}
{'date': '11/09/2023 16:13:04', 'agent_id': 'Monitoring Agent_3', 'detecting': 1, 'id': 'MotionSensor_1', 'state': 'ON', 'type': 'motion'}
{'date': '11/09/2023 16:13:03', 'agent_id': 'Monitoring Agent_2', 'id': 'LightInSensor_1', 'state': 'ON', 'type': 'light_in', 'lux': 356}
{'date': '11/09/2023 16:13:03', 'agent_id': 'Monitoring Agent_1', 'temperature': 37, 'id': 'TempSensor_1', 'state': 'ON', 'type': 'temperature'}

# Rule 2 activated: turning ON the AirConditioner_1

# Rule 3 activated: closing the Door_1

*********************************  R O U N D    3  **********************************

------ STATUS OF THINGS ------
{'id': 'AirConditioner_1', 'type': 'air_conditioner', 'date': '11/09/2023 16:13:14', 'state': 'ON'}
{'id': 'Bulb_1', 'type': 'bulb', 'date': '11/09/2023 16:13:13', 'state': 'OFF'}
{'id': 'Door_1', 'type': 'door', 'date': '11/09/2023 16:13:13', 'state': 'CLOSED'}
{'id': 'Blind_1', 'type': 'blind', 'date': '11/09/2023 16:13:13', 'state': 'CLOSED'}

------ STATUS OF SENSORS ------
{'date': '11/09/2023 16:13:14', 'agent_id': 'Monitoring Agent_4', 'id': 'LightOutSensor_1', 'state': 'ON', 'type': 'light_out', 'lux': 348}
{'date': '11/09/2023 16:13:14', 'agent_id': 'Monitoring Agent_3', 'detecting': 1, 'id': 'MotionSensor_1', 'state': 'ON', 'type': 'motion'}
{'date': '11/09/2023 16:13:13', 'agent_id': 'Monitoring Agent_2', 'id': 'LightInSensor_1', 'state': 'ON', 'type': 'light_in', 'lux': 121}
{'date': '11/09/2023 16:13:13', 'agent_id': 'Monitoring Agent_1', 'temperature': 15, 'id': 'TempSensor_1', 'state': 'ON', 'type': 'temperature'}

# Rule 4 activated: opening the Blind_1

*********************************  R O U N D    4  **********************************

------ STATUS OF THINGS ------
{'id': 'Bulb_1', 'type': 'bulb', 'date': '11/09/2023 16:13:19', 'state': 'OFF'}
{'id': 'Door_1', 'type': 'door', 'date': '11/09/2023 16:13:19', 'state': 'CLOSED'}
{'id': 'Blind_1', 'type': 'blind', 'date': '11/09/2023 16:13:19', 'state': 'OPEN'}
{'id': 'AirConditioner_1', 'type': 'air_conditioner', 'date': '11/09/2023 16:13:19', 'state': 'ON'}

------ STATUS OF SENSORS ------
{'date': '11/09/2023 16:13:19', 'agent_id': 'Monitoring Agent_4', 'id': 'LightOutSensor_1', 'state': 'ON', 'type': 'light_out', 'lux': 310}
{'date': '11/09/2023 16:13:19', 'agent_id': 'Monitoring Agent_3', 'detecting': 0, 'id': 'MotionSensor_1', 'state': 'ON', 'type': 'motion'}
{'date': '11/09/2023 16:13:18', 'agent_id': 'Monitoring Agent_2', 'id': 'LightInSensor_1', 'state': 'ON', 'type': 'light_in', 'lux': 250}
{'date': '11/09/2023 16:13:18', 'agent_id': 'Monitoring Agent_1', 'temperature': 17, 'id': 'TempSensor_1', 'state': 'ON', 'type': 'temperature'}

# None of the rules were applied!
```

