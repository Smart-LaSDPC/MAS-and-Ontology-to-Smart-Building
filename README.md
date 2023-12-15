# MAS-and-Ontology-to-Smart-Building

This code handles sensor data and creates instances in the ontology within the laboratory domain. Subsequently, four inference rules are applied to make the environment intelligent and automated:

### \#1 - Turn off the light

This rule is activated when it is detected that the light is on in the environment and there is no presence of people.

\- `Bulb("ON") AND MotionValue("0") -> Bulb("OFF")`

\* For MotionValue, "0" corresponds to no presence, and "1" to presence
  
### \#2 - Turn on the air conditioning

To activate the air conditioning, the environment must have the air conditioning off, with the presence of person(s), and a temperature above 28 °C.

\- `AirConditioning("OFF") AND MotionValue("1") AND TempValue(>="28") -> AirConditioning("ON")`

### \#3 - Close the door

The door will be closed when the air conditioning is on, and the door is open.

\- `Door("OPEN") AND AirConditioning("ON") -> Door("CLOSED")`

### \#4 - Open the blinds

To harness sunlight to illuminate the laboratory, the blinds will be opened under the following conditions: closed blinds, external light intensity greater than 300 lux, internal light intensity less than 200 lux, presence of person(s), and the light off.

\- `Blind("CLOSED") AND LightOutValue(>="300") AND LightInValue(<="200") AND MotionValue("1") -> Blind("OPEN")`
